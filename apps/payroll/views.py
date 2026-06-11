import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import PayrollRun, Payslip

from apps.employees.models import Employee




def _as_float(value, default=0.0):
    try:
        if value in (None, ""):
            return float(default)
        return float(value)
    except (TypeError, ValueError):
        return float(default)


@login_required
@csrf_exempt
def payroll_dashboard(request):
    if request.method == "POST":
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"ok": False, "error": "Invalid JSON payload."}, status=400)

        rows = payload.get("rows") or []
        if not isinstance(rows, list) or not rows:
            return JsonResponse({"ok": False, "error": "No payroll rows supplied."}, status=400)

        period = (payload.get("period") or "June 2026").strip()
        run = PayrollRun.objects.filter(period=period).order_by("-created_at").first()
        if run is None:
            run = PayrollRun.objects.create(period=period, status="COMPLETED")
        elif run.status != "COMPLETED":
            run.status = "COMPLETED"
            run.save(update_fields=["status"])
        created = 0

        for row in rows:
            if not isinstance(row, dict):
                continue

            employee_name = (row.get("name") or row.get("employeeName") or row.get("candidateName") or "").strip()
            if not employee_name:
                continue

            employee_code = (row.get("id") or row.get("employee_code") or "").strip()
            if not employee_code:
                continue

            first_name, last_name = (employee_name.split(" ", 1) + [""])[:2]

            emp, _ = Employee.objects.get_or_create(
                employee_code=employee_code,
                defaults={
                    "first_name": first_name or employee_code,
                    "last_name": last_name,
                    "email": (row.get("email") or "").strip(),
                }
            )

            emp.first_name = first_name or emp.first_name or employee_code
            emp.last_name = last_name or emp.last_name or ""
            emp.email = (row.get("email") or emp.email or "").strip()
            emp.department = (row.get("department") or row.get("location") or emp.department or "").strip()
            emp.designation = (row.get("designation") or emp.designation or "Consultant").strip()
            emp.status = "ACTIVE" if str(row.get("status") or "Active").lower() in {"active", "paid"} else "INACTIVE"
            emp.month = period
            emp.work_location = (row.get("location") or emp.work_location or "").strip()
            emp.account_number = (row.get("accountNumber") or row.get("account_number") or emp.account_number or "").strip()
            emp.ifsc_code = (row.get("ifscCode") or row.get("ifsc_code") or emp.ifsc_code or "").strip()
            emp.bank_name = (row.get("bankName") or row.get("bank_name") or emp.bank_name or "").strip()
            emp.payment_status = (row.get("paymentStatus") or row.get("payment_status") or "Unpaid").strip()
            emp.utr = (row.get("utr") or emp.utr or "").strip()
            emp.is_vendor_staff = True
            emp.hourly_rate = float(row.get("hourlyRate") or row.get("perDayPayment") or emp.hourly_rate or 0)

            decimal_map = {
                "base_salary": row.get("baseSalary") or row.get("base_salary"),
                "working_days": row.get("workingDays") or row.get("working_days"),
                "basic_pay": row.get("basicPay") or row.get("basic_pay"),
                "hra": row.get("hra"),
                "other_allowance": row.get("otherAllowance") or row.get("other_allowance"),
                "stat_bonus": row.get("statBonus") or row.get("stat_bonus"),
                "attendance_bonus": row.get("attendanceBonus") or row.get("attendance_bonus"),
                "leave_encashment": row.get("leaveEncashment") or row.get("leave_encashment"),
                "performance_incentive": row.get("allowance") or row.get("performanceIncentive") or row.get("performance_incentive") or row.get("incentive"),
                "extra_payment": row.get("extraPayment") or row.get("extra_payment"),
                "shipment_incentive": row.get("shipmentIncentive") or row.get("shipment_incentive"),
                "mobile_allowance": row.get("mobileAllowance") or row.get("mobile_allowance"),
                "meal_incentive": row.get("mealIncentive") or row.get("meal_incentive"),
                "group_incentive": row.get("groupIncentive") or row.get("group_incentive"),
                "night_allowance": row.get("nightAllowance") or row.get("night_allowance"),
                "national_holiday_pay": row.get("nationalHolidayPay") or row.get("national_holiday_pay"),
                "retention_bonus": row.get("retentionBonus") or row.get("retention_bonus"),
                "arrear_payment": row.get("arrearPayment") or row.get("arrear_payment"),
                "esi": row.get("esi"),
                "pf": row.get("pf"),
                "lwf": row.get("lwf"),
                "meal_debit": row.get("mealDebit") or row.get("meal_debit"),
                "refyne_debit": row.get("refyneDebit") or row.get("refyne_debit"),
                "advance_salary": row.get("advanceSalary") or row.get("advance_salary"),
                "pt": row.get("pt"),
                "e_bike_debit": row.get("eBikeDebit") or row.get("e_bike_debit"),
                "advance_payments_in_weeks": row.get("advancePaymentsInWeeks") or row.get("advance_payments_in_weeks"),
                "shipment_debit": row.get("shipmentDebit") or row.get("shipment_debit"),
                "accommodation_recovery": row.get("accommodationRecovery") or row.get("accommodation_recovery"),
                "notice_period_deduction": row.get("noticePeriodDeduction") or row.get("notice_period_deduction"),
                "cod_loss": row.get("codLoss") or row.get("cod_loss"),
                "tshirt_recovery": row.get("tshirtRecovery") or row.get("tshirt_recovery"),
                "ewf_deduction": row.get("ewfDeduction") or row.get("ewf_deduction"),
                "tds": row.get("tds"),
                "candidate_payout": row.get("candidatePayout") or row.get("candidate_payout"),
                "service_charge": row.get("serviceCharge") or row.get("service_charge"),
                "gst_amount": row.get("gstAmount") or row.get("gst_amount"),
                "net_pay": row.get("netPay") or row.get("net_pay"),
                "total_payment": row.get("totalPayment") or row.get("total_payment"),
            }
            for field, value in decimal_map.items():
                try:
                    setattr(emp, field, float(value or 0))
                except Exception:
                    setattr(emp, field, 0)
            emp.save()

            gross_pay = _as_float(
                row.get("candidate_payout")
                or row.get("candidatePayout")
                or row.get("grossPay")
                or row.get("gross_pay")
                or row.get("candidate_payout_amount")
            )
            net_pay = _as_float(row.get("net") or row.get("netPay") or row.get("net_pay"))

            Payslip.objects.update_or_create(
                payroll_run=run,
                employee_name=employee_name,
                defaults={
                    "gross_pay": gross_pay,
                    "net_pay": net_pay,
                },
            )
            created += 1

        return JsonResponse({"ok": True, "run_id": run.id, "created": created})

    runs = PayrollRun.objects.order_by("-created_at")[:12]
    # Filter employees who are vendor staff for the current active period
    vendor_employees = Employee.objects.filter(is_vendor_staff=True, month="June 2026").order_by("employee_code")

    payroll_rows = []
    total_gross = 0
    total_tax = 0
    total_net = 0

    for emp in vendor_employees:
        gross_pay = float(emp.candidate_payout or emp.base_salary or 0)
        net_pay = float(emp.net_pay or 0)
        tds = float(emp.tds or round(gross_pay * 0.01, 2))
        service_charge = float(emp.service_charge or 0)
        vendor_payout = gross_pay + service_charge
        gst = float(emp.gst_amount or round(vendor_payout * 0.18, 2))
        total_payment = float(emp.total_payment or round(vendor_payout + gst, 2))

        payroll_rows.append({
            "id": emp.employee_code,
            "name": f"{emp.first_name} {emp.last_name}".strip(),
            "designation": emp.designation or "Consultant",
            "location": emp.work_location or "Payroll",
            "working_days": float(emp.working_days or 0),
            "base_salary": float(emp.base_salary or 0),
            "per_day": float(emp.hourly_rate or 0),
            "incentive": float(emp.performance_incentive or 0),
            "candidate_payout": gross_pay,
            "tds": tds,
            "net": net_pay,
            "service_charge": service_charge,
            "vendor_payout": vendor_payout,
            "gst": gst,
            "total_payment": total_payment,
            "status": emp.payment_status or "Paid",
            "utr": emp.utr or "—",
            "payroll_run": emp.month or "June 2026",
            "slip_id": emp.employee_code,
        })

        total_gross += gross_pay
        total_tax += tds
        total_net += total_payment

    return render(request, "payroll.html", {
        "runs": runs,
        "payroll_rows": payroll_rows,
        "payroll_rows_json": payroll_rows,
        "payroll_totals": {
            "gross": total_gross,
            "tax": total_tax,
            "net": total_net,
        },
        "active_page": "payroll",
        "active_period": "June 2026",
        "current_time": timezone.localtime().strftime("%d/%m/%Y | %H:%M"),
    })

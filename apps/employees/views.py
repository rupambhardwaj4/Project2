from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Employee
import json


@login_required
@csrf_exempt
def directory(request):
    if request.method == "POST":
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"ok": False, "error": "Invalid JSON payload."}, status=400)

        employee_code = (payload.get("id") or payload.get("employee_code") or "").strip()
        if not employee_code:
            return JsonResponse({"ok": False, "error": "Employee code is required."}, status=400)

        full_name = (payload.get("name") or "").strip()
        first_name, last_name = (full_name.split(" ", 1) + [""])[:2] if full_name else ("", "")
        emp, created = Employee.objects.get_or_create(employee_code=employee_code, defaults={
            "first_name": first_name or employee_code,
            "last_name": last_name,
            "email": (payload.get("email") or "").strip(),
        })

        emp.first_name = first_name or emp.first_name or employee_code
        emp.last_name = last_name or emp.last_name or ""
        emp.email = (payload.get("email") or emp.email or "").strip()
        emp.department = (payload.get("department") or payload.get("centre") or emp.department or "").strip()
        emp.designation = (payload.get("role") or emp.designation or "Consultant").strip()
        emp.status = "ACTIVE" if str(payload.get("status") or "Active").lower() in {"active", "paid"} else "INACTIVE"
        emp.month = (payload.get("month") or emp.month or "June 2026").strip()
        emp.work_location = (payload.get("workLocation") or payload.get("centre") or emp.work_location or "").strip()
        emp.account_number = (payload.get("accountNumber") or emp.account_number or "").strip()
        emp.ifsc_code = (payload.get("ifscCode") or emp.ifsc_code or "").strip()
        emp.bank_name = (payload.get("bankName") or emp.bank_name or "").strip()
        emp.payment_status = (payload.get("paymentStatus") or emp.payment_status or "Unpaid").strip()
        emp.utr = (payload.get("utr") or emp.utr or "").strip()

        decimal_map = {
            "base_salary": payload.get("baseSalary"),
            "working_days": payload.get("hoursWorked"),
            "basic_pay": payload.get("basicPay"),
            "hra": payload.get("hra"),
            "other_allowance": payload.get("otherAllowance"),
            "stat_bonus": payload.get("statBonus"),
            "attendance_bonus": payload.get("attendanceBonus"),
            "leave_encashment": payload.get("leaveEncashment"),
            "performance_incentive": payload.get("allowance"),
            "extra_payment": payload.get("extraPayment"),
            "shipment_incentive": payload.get("shipmentIncentive"),
            "mobile_allowance": payload.get("mobileAllowance"),
            "meal_incentive": payload.get("mealIncentive"),
            "group_incentive": payload.get("groupIncentive"),
            "night_allowance": payload.get("nightAllowance"),
            "national_holiday_pay": payload.get("nationalHolidayPay"),
            "retention_bonus": payload.get("retentionBonus"),
            "arrear_payment": payload.get("arrearPayment"),
            "esi": payload.get("esi"),
            "pf": payload.get("pf"),
            "lwf": payload.get("lwf"),
            "meal_debit": payload.get("mealDebit"),
            "refyne_debit": payload.get("refyneDebit"),
            "advance_salary": payload.get("advanceSalary"),
            "pt": payload.get("pt"),
            "e_bike_debit": payload.get("eBikeDebit"),
            "advance_payments_in_weeks": payload.get("advancePaymentsInWeeks"),
            "shipment_debit": payload.get("shipmentDebit"),
            "accommodation_recovery": payload.get("accommodationRecovery"),
            "notice_period_deduction": payload.get("noticePeriodDeduction"),
            "cod_loss": payload.get("codLoss"),
            "tshirt_recovery": payload.get("tshirtRecovery"),
            "ewf_deduction": payload.get("ewfDeduction"),
            "tds": payload.get("tds"),
            "candidate_payout": payload.get("candidatePayout"),
            "service_charge": payload.get("serviceCharge"),
            "gst_amount": payload.get("gstAmount"),
            "net_pay": payload.get("netPay"),
            "total_payment": payload.get("totalPayment"),
        }
        for field, value in decimal_map.items():
            try:
                setattr(emp, field, float(value or 0))
            except Exception:
                setattr(emp, field, 0)

        emp.save()
        return JsonResponse({"ok": True, "employee_code": emp.employee_code, "created": created})

    employees = Employee.objects.filter(is_vendor_staff=False).order_by("employee_code")
    employees_data = [
        {
            "id": employee.employee_code,
            "name": f"{employee.first_name} {employee.last_name}".strip(),
            "email": employee.email,
            "phone": getattr(employee.user, "phone", "") or "",
            "centre": employee.department or "",
            "department": employee.department or "",
            "month": employee.month or "June 2026",
            "status": "Active" if employee.status.upper() == "ACTIVE" else employee.status.title(),
            "baseSalary": float(employee.base_salary or 0),
            "accountNumber": employee.account_number or "",
            "ifscCode": employee.ifsc_code or "",
            "bankName": employee.bank_name or "",
            "utr": employee.utr or "",
            "role": employee.designation or "Consultant",
            "hoursWorked": float(employee.working_days or 0),
            "timesheetStatus": "Uploaded",
            "allowance": float(employee.performance_incentive or 0),
            "deductions": float(employee.tds or 0),
            "hourlyRate": 0,
            "paymentStatus": employee.payment_status or employee.status.title(),
            "workLocation": employee.work_location or "",
            "basicPay": float(employee.basic_pay or 0),
            "hra": float(employee.hra or 0),
            "otherAllowance": float(employee.other_allowance or 0),
            "statBonus": float(employee.stat_bonus or 0),
            "attendanceBonus": float(employee.attendance_bonus or 0),
            "leaveEncashment": float(employee.leave_encashment or 0),
            "performanceIncentive": float(employee.performance_incentive or 0),
            "extraPayment": float(employee.extra_payment or 0),
            "shipmentIncentive": float(employee.shipment_incentive or 0),
            "mobileAllowance": float(employee.mobile_allowance or 0),
            "mealIncentive": float(employee.meal_incentive or 0),
            "groupIncentive": float(employee.group_incentive or 0),
            "nightAllowance": float(employee.night_allowance or 0),
            "nationalHolidayPay": float(employee.national_holiday_pay or 0),
            "retentionBonus": float(employee.retention_bonus or 0),
            "arrearPayment": float(employee.arrear_payment or 0),
            "esi": float(employee.esi or 0),
            "pf": float(employee.pf or 0),
            "lwf": float(employee.lwf or 0),
            "mealDebit": float(employee.meal_debit or 0),
            "refyneDebit": float(employee.refyne_debit or 0),
            "advanceSalary": float(employee.advance_salary or 0),
            "pt": float(employee.pt or 0),
            "eBikeDebit": float(employee.e_bike_debit or 0),
            "advancePaymentsInWeeks": float(employee.advance_payments_in_weeks or 0),
            "shipmentDebit": float(employee.shipment_debit or 0),
            "accommodationRecovery": float(employee.accommodation_recovery or 0),
            "noticePeriodDeduction": float(employee.notice_period_deduction or 0),
            "codLoss": float(employee.cod_loss or 0),
            "tshirtRecovery": float(employee.tshirt_recovery or 0),
            "ewfDeduction": float(employee.ewf_deduction or 0),
            "tds": float(employee.tds or 0),
            "candidatePayout": float(employee.candidate_payout or 0),
            "serviceCharge": float(employee.service_charge or 0),
            "gstAmount": float(employee.gst_amount or 0),
            "netPay": float(employee.net_pay or 0),
            "totalPayment": float(employee.total_payment or 0),
        }
        for employee in employees
    ]
    return render(request, "directory.html", {
        "employees": employees,
        "employees_data": employees_data,
        "active_page": "directory",
        "active_period": "June 2026",
        "current_time": timezone.localtime().strftime("%d/%m/%Y | %H:%M"),
    })

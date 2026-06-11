from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
from decimal import Decimal
from apps.employees.models import Employee
from apps.payroll.models import PayrollRun
from .models import CompanyProfile

def _serialize_employee(emp):
    if not emp:
        return None
    return {
        "id": emp.employee_code,
        "name": f"{emp.first_name} {emp.last_name}".strip(),
        "email": emp.email,
        "phone": getattr(emp.user, "phone", "") or "",
        "centre": emp.department or "",
        "department": emp.department or "",
        "month": emp.month or "June 2026",
        "status": "Active" if emp.status.upper() == "ACTIVE" else emp.status.title(),
        "baseSalary": float(emp.base_salary or 0),
        "accountNumber": emp.account_number or "",
        "ifscCode": emp.ifsc_code or "",
        "bankName": emp.bank_name or "",
        "utr": emp.utr or "",
        "role": emp.designation or "Consultant",
        "hoursWorked": float(emp.working_days or 0),
        "workingDays": float(emp.working_days or 0),
        "timesheetStatus": "Uploaded",
        "allowance": float(emp.performance_incentive or 0),
        "deductions": float(emp.tds or 0),
        "hourlyRate": float(emp.hourly_rate or 0),
        "perDayPayment": float(emp.hourly_rate or 0),
        "paymentStatus": emp.payment_status or emp.status.title(),
        "workLocation": emp.work_location or "",
        "isVendorStaff": emp.is_vendor_staff,
        "slip": {
            "basic_pay": float(emp.basic_pay or 0),
            "hra": float(emp.hra or 0),
            "other_allowance": float(emp.other_allowance or 0),
            "stat_bonus": float(emp.stat_bonus or 0),
            "attendance_bonus": float(emp.attendance_bonus or 0),
            "leave_encashment": float(emp.leave_encashment or 0),
            "performance_incentive": float(emp.performance_incentive or 0),
            "extra_payment": float(emp.extra_payment or 0),
            "shipment_incentive": float(emp.shipment_incentive or 0),
            "mobile_allowance": float(emp.mobile_allowance or 0),
            "meal_incentive": float(emp.meal_incentive or 0),
            "group_incentive": float(emp.group_incentive or 0),
            "night_allowance": float(emp.night_allowance or 0),
            "national_holiday_pay": float(emp.national_holiday_pay or 0),
            "retention_bonus": float(emp.retention_bonus or 0),
            "arrear_payment": float(emp.arrear_payment or 0),
            "esi": float(emp.esi or 0),
            "pf": float(emp.pf or 0),
            "lwf": float(emp.lwf or 0),
            "meal_debit": float(emp.meal_debit or 0),
            "refyne_debit": float(emp.refyne_debit or 0),
            "advance_salary": float(emp.advance_salary or 0),
            "pt": float(emp.pt or 0),
            "e_bike_debit": float(emp.e_bike_debit or 0),
            "advance_payments_in_weeks": float(emp.advance_payments_in_weeks or 0),
            "shipment_debit": float(emp.shipment_debit or 0),
            "accommodation_recovery": float(emp.accommodation_recovery or 0),
            "notice_period_deduction": float(emp.notice_period_deduction or 0),
            "cod_loss": float(emp.cod_loss or 0),
            "tshirt_recovery": float(emp.tshirt_recovery or 0),
            "ewf_deduction": float(emp.ewf_deduction or 0),
            "tds": float(emp.tds or 0),
            "candidate_payout": float(emp.candidate_payout or 0),
            "service_charge": float(emp.service_charge or 0),
            "gst_amount": float(emp.gst_amount or 0),
            "net_pay": float(emp.net_pay or 0),
            "total_payment": float(emp.total_payment or 0),
            "invoice_number": emp.invoice_number or "",
            "invoice_topic": emp.invoice_topic or "",
            "invoice_status": emp.invoice_status or "",
        },
    }


def _pick(payload, *keys, default=""):
    for key in keys:
        value = payload.get(key)
        if value not in (None, ""):
            return value
    return default


def landing(request):
    if request.user.is_authenticated:
        return render(request, "dashboard.html", {
            "active_page": "dashboard",
            "active_period": "June 2026",
            "current_time": timezone.localtime().strftime("%d/%m/%Y | %H:%M"),
        })
    return render(request, "index.html", {})


@login_required
def dashboard(request):
    employees = Employee.objects.all().order_by("-created_at")
    active_employees = employees.filter(status__iexact="ACTIVE")
    inactive_employees = employees.exclude(status__iexact="ACTIVE")
    payroll_runs = PayrollRun.objects.order_by("-created_at")

    department_counts = {}
    for emp in employees:
        dept = emp.department or "Unassigned"
        department_counts[dept] = department_counts.get(dept, 0) + 1

    department_stats = [
        {"name": name, "count": count}
        for name, count in sorted(department_counts.items(), key=lambda item: item[1], reverse=True)
    ]

    recent_employees = employees[:6]
    total_payroll = 0
    for idx, emp in enumerate(employees, start=1):
        base_salary = float(emp.base_salary or (24000 + (idx * 1500)))
        working_days = float(emp.working_days or (22 if emp.status.upper() == "ACTIVE" else 0))
        per_day = round(base_salary / 30, 2) if base_salary else 0
        incentive = float(emp.performance_incentive or (500 if emp.status.upper() == "ACTIVE" else 0))
        service_charge = float(emp.service_charge or round(base_salary * 0.10, 2))
        candidate_payout = float(emp.candidate_payout or round((working_days * per_day) + incentive, 2))
        tds = float(emp.tds or round(candidate_payout * 0.01, 2))
        vendor_payout = candidate_payout + service_charge
        gst = float(emp.gst_amount or round(vendor_payout * 0.18, 2))
        total_payroll += float(emp.total_payment or round(vendor_payout + gst, 2))

    return render(request, "dashboard.html", {
        "active_page": "dashboard",
        "active_period": "June 2026",
        "current_time": timezone.localtime().strftime("%d/%m/%Y | %H:%M"),
        "total_employees": employees.count(),
        "active_employees": active_employees.count(),
        "inactive_employees": inactive_employees.count(),
        "timesheets_processed": active_employees.count(),
        "last_payroll_run": payroll_runs.first().created_at.strftime("%d %b %Y") if payroll_runs.exists() else "Never",
        "total_payroll": f"₹{total_payroll:,.2f}",
        "department_stats_json": department_stats,
        "recent_employees": recent_employees,
    })


@login_required
@csrf_exempt
def settings_page(request):
    if request.method == "POST":
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"ok": False, "error": "Invalid JSON payload."}, status=400)
        
        company = CompanyProfile.load_cached()
        
        # Map camelCase keys to snake_case database fields
        mapping = {
            "shortName": "short_name",
            "fullLegalName": "full_legal_name",
            "headOfficeAddress": "head_office_address",
            "supportEmail": "support_email",
            "contactPhone": "contact_phone",
            "logoInitials": "logo_initials",
            "primaryColor": "primary_color",
            "sidebarColor": "sidebar_color",
            "gstin": "gstin",
            "stateCode": "state_code",
            "websiteUrl": "website_url",
            "logoImage": "logo_image",
            "signatureImage": "signature_image",
            "sealImage": "seal_image",
            "accountName": "account_name",
            "accountNo": "account_no",
            "ifscCode": "ifsc_code",
            "bankName": "bank_name",
            "branchName": "branch_name",
            "signatoryName": "signatory_name",
        }
        
        for key, field in mapping.items():
            if key in payload:
                setattr(company, field, payload[key])
                
        company.save()
        return JsonResponse({"ok": True})
        
    return render(request, "settings.html", {
        "active_page": "settings",
        "active_period": "June 2026",
        "current_time": timezone.localtime().strftime("%d/%m/%Y | %H:%M"),
    })


@login_required
@csrf_exempt
def salary_slip(request):
    if request.method == "POST":
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"ok": False, "error": "Invalid JSON payload."}, status=400)

        employee_code = str(_pick(payload, "employee_code", "employeeCode", "id")).strip()
        if not employee_code:
            return JsonResponse({"ok": False, "error": "Employee code is required."}, status=400)

        try:
            emp = Employee.objects.get(employee_code=employee_code)
        except Employee.DoesNotExist:
            emp = Employee(employee_code=employee_code)

        # Parse profile details
        first_name = payload.get("first_name", "").strip()
        last_name = payload.get("last_name", "").strip()
        if "name" in payload and not (first_name or last_name):
            full_name = payload.get("name", "").strip()
            parts = full_name.split(" ", 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ""

        if first_name:
            emp.first_name = first_name
        if last_name:
            emp.last_name = last_name

        # Enforce non-empty fields for DB constraints on new employees
        if not emp.first_name:
            emp.first_name = "New"
        if not emp.last_name:
            emp.last_name = "Employee"
        if not emp.email:
            emp.email = payload.get("email", "").strip() or f"{employee_code.lower()}@qtconsultancy.in"

        if "department" in payload:
            emp.department = payload.get("department", "").strip()
        if "designation" in payload:
            emp.designation = payload.get("designation", "").strip()
        if "status" in payload:
            emp.status = payload.get("status", "ACTIVE").strip()
        if "is_vendor_staff" in payload:
            emp.is_vendor_staff = bool(payload.get("is_vendor_staff"))
        if "hourly_rate" in payload:
            try:
                emp.hourly_rate = Decimal(str(payload.get("hourly_rate") or 0))
            except Exception:
                pass

        payroll_fields = [
            "month", "work_location", "account_number", "ifsc_code", "bank_name",
            "payment_status", "utr", "invoice_number", "invoice_topic", "invoice_status",
        ]
        decimal_fields = [
            "base_salary", "working_days", "basic_pay", "hra", "other_allowance", "stat_bonus",
            "attendance_bonus", "leave_encashment", "performance_incentive", "extra_payment",
            "shipment_incentive", "mobile_allowance", "meal_incentive", "group_incentive",
            "night_allowance", "national_holiday_pay", "retention_bonus", "arrear_payment",
            "esi", "pf", "lwf", "meal_debit", "refyne_debit", "advance_salary", "pt",
            "e_bike_debit", "advance_payments_in_weeks", "shipment_debit",
            "accommodation_recovery", "notice_period_deduction", "cod_loss", "tshirt_recovery",
            "ewf_deduction", "tds", "candidate_payout", "service_charge", "gst_amount",
            "net_pay", "total_payment",
        ]

        for field in payroll_fields:
            if field in payload:
                setattr(emp, field, (payload.get(field) or "").strip() if isinstance(payload.get(field), str) else payload.get(field))
        for field in decimal_fields:
            if field in payload:
                try:
                    setattr(emp, field, Decimal(str(payload.get(field) or 0)))
                except Exception:
                    setattr(emp, field, Decimal("0"))

        alias_map = {
            "candidate_payout": ["candidate_payout", "candidatePayout", "gross_pay", "grossPay"],
            "net_pay": ["net_pay", "netPay", "net"],
            "tds": ["tds", "taxAmount", "tax_amount"],
            "service_charge": ["service_charge", "serviceCharge"],
            "gst_amount": ["gst_amount", "gstAmount", "gst"],
        }
        for field, aliases in alias_map.items():
            value = None
            for alias in aliases:
                if alias in payload and payload.get(alias) not in (None, ""):
                    value = payload.get(alias)
                    break
            if value is not None:
                try:
                    setattr(emp, field, Decimal(str(value)))
                except Exception:
                    setattr(emp, field, Decimal("0"))

        emp.save()
        return JsonResponse({"ok": True, "employee_code": emp.employee_code, "employee": _serialize_employee(emp)})

    selected_code = (request.GET.get("id") or "").strip()
    selected_employee = None
    if selected_code:
        selected_employee = Employee.objects.filter(employee_code=selected_code).first()
    if not selected_employee:
        selected_employee = Employee.objects.order_by("employee_code").first()

    employee_payload = _serialize_employee(selected_employee)

    all_employees = Employee.objects.all().order_by("employee_code")
    all_employees_data = [
        _serialize_employee(emp) for emp in all_employees if emp
    ]

    return render(request, "salaryslip.html", {
        "active_page": "salaryslip",
        "active_period": "June 2026",
        "current_time": timezone.localtime().strftime("%d/%m/%Y | %H:%M"),
        "selected_employee_data": employee_payload or {},
        "all_employees_data": all_employees_data,
    })

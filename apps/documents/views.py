from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Invoice
from apps.employees.models import Employee


def _pick(payload, *keys, default=""):
    for key in keys:
        value = payload.get(key)
        if value not in (None, ""):
            return value
    return default


@login_required
@csrf_exempt
def invoices(request):
    if request.method == "POST":
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"ok": False, "error": "Invalid JSON payload."}, status=400)

        invoice_number = (payload.get("invoiceNum") or payload.get("invoice_number") or "").strip()
        if not invoice_number:
            return JsonResponse({"ok": False, "error": "Invoice number is required."}, status=400)

        invoice, _ = Invoice.objects.update_or_create(
            invoice_number=invoice_number,
            defaults={
                "owner": request.user,
                "employee_code": str(_pick(payload, "employeeCode", "employee_code")).strip(),
                "invoice_date": _pick(payload, "invoiceDate", "invoice_date", default=timezone.localdate()),
                "topic": str(_pick(payload, "topic", "invoice_topic")).strip(),
                "client_name": str(_pick(payload, "clientName", "client_name")).strip(),
                "client_address": str(_pick(payload, "clientAddress", "client_address")).strip(),
                "client_gstin": str(_pick(payload, "clientGstin", "client_gstin")).strip(),
                "client_state": str(_pick(payload, "clientState", "client_state")).strip(),
                "client_state_code": str(_pick(payload, "clientStateCode", "client_state_code")).strip(),
                "supply_state": str(_pick(payload, "supplyState", "supply_state")).strip(),
                "status": str(_pick(payload, "status", default="UNPAID")).strip(),
                "gross_total": float(_pick(payload, "grossTotal", "gross_total", default=0) or 0),
                "tax_total": float(_pick(payload, "taxTotal", "tax_total", default=0) or 0),
                "final_total": float(_pick(payload, "finalTotal", "final_total", default=0) or 0),
                
                # New fields from handwritten list
                "source_company": str(_pick(payload, "sourceCompany", "source_company")).strip(),
                "destination_company": str(_pick(payload, "destinationCompany", "destination_company", "clientName", "client_name")).strip(),
                "gstin_a": str(_pick(payload, "gstinA", "gstin_a", "gstin")).strip(),
                "state_code_a": str(_pick(payload, "stateCodeA", "state_code_a", "stateCode")).strip(),
                "website": str(_pick(payload, "website", "websiteUrl", "website_url")).strip(),
                "location": str(_pick(payload, "location", "headOfficeAddress", "head_office_address")).strip(),
                "state": str(_pick(payload, "state", "clientState", "client_state", "supplyState", "supply_state")).strip(),
                "reverse_charge": str(_pick(payload, "reverseCharge", "reverse_charge", default="No")).strip(),
                "state_code": str(_pick(payload, "stateCode", "clientStateCode", "client_state_code")).strip(),
                "taxable_amt_before_tax": float(_pick(payload, "taxableAmtBeforeTax", "taxable_amt_before_tax", "grossTotal", "gross_total", default=0) or 0),
                "total_tax_amt": float(_pick(payload, "totalTaxAmt", "total_tax_amt", "taxTotal", "tax_total", default=0) or 0),
                "final_invoice_amt": float(_pick(payload, "finalInvoiceAmt", "final_invoice_amt", "finalTotal", "final_total", default=0) or 0),
                "balance_due": float(_pick(payload, "balanceDue", "balance_due", default=0) or 0),
                "account_name": str(_pick(payload, "accountName", "account_name")).strip(),
                "account_no": str(_pick(payload, "accountNo", "account_no")).strip(),
                "ifsc_code": str(_pick(payload, "ifscCode", "ifsc_code", "ifsc")).strip(),
                "bank_name": str(_pick(payload, "bankName", "bank_name")).strip(),
                "branch_name": str(_pick(payload, "branchName", "branch_name")).strip(),
                
                "payload": payload,
            },
        )
        return JsonResponse({"ok": True, "invoice_number": invoice.invoice_number, "id": invoice.id})

    employees = Employee.objects.all().order_by("employee_code")
    invoices = Invoice.objects.order_by("-created_at")
    employees_data = [
        {
            "id": employee.employee_code,
            "name": f"{employee.first_name} {employee.last_name}".strip(),
            "email": employee.email,
            "department": employee.department or "",
            "status": "Active" if employee.status.upper() == "ACTIVE" else employee.status.title(),
            "baseSalary": float(employee.base_salary or 0),
            "paymentStatus": employee.payment_status or employee.status.title(),
        }
        for employee in employees
    ]
    invoices_data = [
        {
            "id": invoice.id,
            "employeeCode": invoice.employee_code,
            "invoiceNum": invoice.invoice_number,
            "invoiceDate": invoice.invoice_date.isoformat(),
            "topic": invoice.topic,
            "clientName": invoice.client_name,
            "clientAddress": invoice.client_address,
            "clientGstin": invoice.client_gstin,
            "clientState": invoice.client_state,
            "clientStateCode": invoice.client_state_code,
            "supplyState": invoice.supply_state,
            "status": invoice.status,
            "grossTotal": float(invoice.gross_total or 0),
            "taxTotal": float(invoice.tax_total or 0),
            "finalTotal": float(invoice.final_total or 0),
            
            # New serialized fields
            "sourceCompany": invoice.source_company,
            "destinationCompany": invoice.destination_company,
            "gstinA": invoice.gstin_a,
            "stateCodeA": invoice.state_code_a,
            "website": invoice.website,
            "location": invoice.location,
            "state": invoice.state,
            "reverseCharge": invoice.reverse_charge,
            "stateCode": invoice.state_code,
            "taxableAmtBeforeTax": float(invoice.taxable_amt_before_tax or 0),
            "totalTaxAmt": float(invoice.total_tax_amt or 0),
            "finalInvoiceAmt": float(invoice.final_invoice_amt or 0),
            "balanceDue": float(invoice.balance_due or 0),
            "accountName": invoice.account_name,
            "accountNo": invoice.account_no,
            "ifscCode": invoice.ifsc_code,
            "bankName": invoice.bank_name,
            "branchName": invoice.branch_name,
            
            "payload": invoice.payload or {},
        }
        for invoice in invoices
    ]
    return render(request, "invoices.html", {
        "active_period": "June 2026",
        "current_time": timezone.localtime().strftime("%d/%m/%Y | %H:%M"),
        "employees_data": employees_data,
        "invoices_data": invoices_data,
    })

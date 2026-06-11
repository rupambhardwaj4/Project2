from django.db import models


class PayrollRun(models.Model):
    period = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="DRAFT")


class Payslip(models.Model):
    payroll_run = models.ForeignKey(PayrollRun, on_delete=models.CASCADE, related_name="payslips")
    employee_name = models.CharField(max_length=200)
    gross_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)

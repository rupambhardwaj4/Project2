from django.conf import settings
from django.db import models


class Document(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="documents/")
    created_at = models.DateTimeField(auto_now_add=True)


class Invoice(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    employee_code = models.CharField(max_length=32, blank=True)
    invoice_number = models.CharField(max_length=64, unique=True)
    invoice_date = models.DateField()
    topic = models.CharField(max_length=255, blank=True)
    client_name = models.CharField(max_length=255, blank=True)
    client_address = models.TextField(blank=True)
    client_gstin = models.CharField(max_length=32, blank=True)
    client_state = models.CharField(max_length=64, blank=True)
    client_state_code = models.CharField(max_length=16, blank=True)
    supply_state = models.CharField(max_length=64, blank=True)
    status = models.CharField(max_length=32, default="UNPAID")
    gross_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    final_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Source & Destination metadata
    source_company = models.CharField(max_length=255, default="", blank=True)
    destination_company = models.CharField(max_length=255, default="", blank=True)
    gstin_a = models.CharField(max_length=32, default="", blank=True)
    state_code_a = models.CharField(max_length=16, default="", blank=True)
    website = models.CharField(max_length=255, default="", blank=True)
    location = models.TextField(default="", blank=True)
    
    # Invoice level details
    state = models.CharField(max_length=64, default="", blank=True)
    reverse_charge = models.CharField(max_length=32, default="No", blank=True)
    state_code = models.CharField(max_length=16, default="", blank=True)
    
    # Financial summaries
    taxable_amt_before_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_tax_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    final_invoice_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance_due = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Bank & Payment details
    account_name = models.CharField(max_length=255, default="", blank=True)
    account_no = models.CharField(max_length=120, default="", blank=True)
    ifsc_code = models.CharField(max_length=64, default="", blank=True)
    bank_name = models.CharField(max_length=255, default="", blank=True)
    branch_name = models.CharField(max_length=255, default="", blank=True)

    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

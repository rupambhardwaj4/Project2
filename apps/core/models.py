from django.db import models


class CompanyProfile(models.Model):
    short_name = models.CharField(max_length=120, default="QT Consultancy")
    full_legal_name = models.CharField(max_length=255, default="QT Consultancy Private Limited")
    head_office_address = models.TextField(default="12th Floor, DLF Cyber City, Sector 21, Gurgaon, Haryana - 122002")
    support_email = models.EmailField(default="hr@qtconsultancy.in")
    contact_phone = models.CharField(max_length=32, default="+91 9899844927")
    logo_initials = models.CharField(max_length=8, default="QT")
    primary_color = models.CharField(max_length=32, default="#88BDF2")
    sidebar_color = models.CharField(max_length=32, default="#384959")
    gstin = models.CharField(max_length=20, default="09AABCQ0892L1Z0")
    state_code = models.CharField(max_length=4, default="09")
    website_url = models.URLField(default="https://qtconsultancy.in")
    
    # New Image fields (Base64 data)
    logo_image = models.TextField(null=True, blank=True)
    signature_image = models.TextField(null=True, blank=True)
    seal_image = models.TextField(null=True, blank=True)

    apply_signature_to_invoice = models.BooleanField(default=True)
    apply_signature_to_salary_slip = models.BooleanField(default=True)
    apply_seal_to_invoice = models.BooleanField(default=True)
    apply_seal_to_salary_slip = models.BooleanField(default=True)

    # New Bank details & Signatory fields
    account_name = models.CharField(max_length=255, default="QT Consultancy Private Limited")
    account_no = models.CharField(max_length=120, default="")
    ifsc_code = models.CharField(max_length=64, default="")
    bank_name = models.CharField(max_length=255, default="")
    branch_name = models.CharField(max_length=255, default="")
    signatory_name = models.CharField(max_length=255, default="QT Consultancy")
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company Profile"

    def to_dict(self):
        return {
            "shortName": self.short_name,
            "fullLegalName": self.full_legal_name,
            "headOfficeAddress": self.head_office_address,
            "supportEmail": self.support_email,
            "contactPhone": self.contact_phone,
            "logoInitials": self.logo_initials,
            "primaryColor": self.primary_color,
            "sidebarColor": self.sidebar_color,
            "gstin": self.gstin,
            "stateCode": self.state_code,
            "websiteUrl": self.website_url,
            "logoImage": self.logo_image or None,
            "signatureImage": self.signature_image or None,
            "sealImage": self.seal_image or None,
            "applySignatureToInvoice": self.apply_signature_to_invoice,
            "applySignatureToSalarySlip": self.apply_signature_to_salary_slip,
            "applySealToInvoice": self.apply_seal_to_invoice,
            "applySealToSalarySlip": self.apply_seal_to_salary_slip,
            "accountName": self.account_name,
            "accountNo": self.account_no,
            "ifscCode": self.ifsc_code,
            "bankName": self.bank_name,
            "branchName": self.branch_name,
            "signatoryName": self.signatory_name,
        }

    @classmethod
    def load_cached(cls):
        obj = cls.objects.order_by("id").first()
        if obj:
            return obj
        # Return a transient instance with defaults.
        # It's better to save it to DB if it doesn't exist so we always have a record.
        try:
            # Only save if we are inside a context that allows DB write (django check runs migrates, etc.)
            obj = cls.objects.create()
            return obj
        except Exception:
            return cls()


from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CompanyProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("short_name", models.CharField(default="QT Consultancy", max_length=120)),
                ("full_legal_name", models.CharField(default="QT Consultancy Private Limited", max_length=255)),
                ("head_office_address", models.TextField(default="12th Floor, DLF Cyber City, Sector 21, Gurgaon, Haryana - 122002")),
                ("support_email", models.EmailField(default="hr@qtconsultancy.in", max_length=254)),
                ("contact_phone", models.CharField(default="+91 9899844927", max_length=32)),
                ("logo_initials", models.CharField(default="QT", max_length=8)),
                ("primary_color", models.CharField(default="#88BDF2", max_length=32)),
                ("sidebar_color", models.CharField(default="#384959", max_length=32)),
                ("gstin", models.CharField(default="09AABCQ0892L1Z0", max_length=20)),
                ("state_code", models.CharField(default="09", max_length=4)),
                ("website_url", models.URLField(default="https://qtconsultancy.in")),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]

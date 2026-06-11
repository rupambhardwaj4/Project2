from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="PayrollRun",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("period", models.CharField(max_length=32)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("status", models.CharField(default="DRAFT", max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Payslip",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("employee_name", models.CharField(max_length=200)),
                ("gross_pay", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("net_pay", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("payroll_run", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="payslips", to="payroll.payrollrun")),
            ],
        ),
    ]

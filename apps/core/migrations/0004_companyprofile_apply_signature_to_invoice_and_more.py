from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_companyprofile_account_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyprofile',
            name='apply_signature_to_invoice',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='apply_signature_to_salary_slip',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='apply_seal_to_invoice',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='apply_seal_to_salary_slip',
            field=models.BooleanField(default=True),
        ),
    ]

from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_default_admin(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    if not User.objects.filter(email__iexact="admin@company.com").exists():
        user = User(
            username="admin",
            email="admin@company.com",
            first_name="Admin",
            last_name="User",
            is_staff=True,
            is_superuser=True,
            is_active=True,
            role="ADMIN",
            password=make_password("admin123"),
        )
        user.save()


def remove_default_admin(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    User.objects.filter(email__iexact="admin@company.com").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_default_admin, remove_default_admin),
    ]

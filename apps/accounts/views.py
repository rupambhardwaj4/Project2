from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == "POST":
        email_or_username = (request.POST.get("email") or "").strip()
        password = request.POST.get("password") or ""

        user = authenticate(
            request,
            username=email_or_username,
            password=password,
        )

        if user is None and email_or_username:
            User = get_user_model()
            try:
                candidate = User.objects.get(email__iexact=email_or_username)
            except User.DoesNotExist:
                candidate = None
            if candidate is not None and candidate.check_password(password):
                user = candidate

        if user:
            login(request, user)
            return redirect("/dashboard/")
        return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")

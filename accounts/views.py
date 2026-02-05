from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect

def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "Email and password are required")
            return redirect("/accounts/register/")

        if User.objects.filter(username=email).exists():
            messages.error(request, "User already exists")
            return redirect("/accounts/register/")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        login(
            request,
            user,
            backend="django.contrib.auth.backends.ModelBackend"
        )

        messages.success(request, "Account created successfully")
        return redirect("/dashboard/user/")

    return render(request, "accounts/register.html")


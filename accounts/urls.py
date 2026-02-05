from django.urls import path
from . import views

app_name = "accounts"   # ✅ THIS LINE FIXES IT

urlpatterns = [
    path("register/", views.register, name="register"),
]

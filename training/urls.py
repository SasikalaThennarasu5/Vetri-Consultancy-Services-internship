from django.urls import path
from . import views
from .views import download_certificate

app_name = "training"

urlpatterns = [
    path("", views.training_home, name="home"),
    path(
        "certificate/<int:enrollment_id>/",
        download_certificate,
        name="certificate"
    ),
]


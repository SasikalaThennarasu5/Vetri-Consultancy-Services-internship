from django.urls import path
from . import views

app_name = "jobs"   # 🔴 THIS LINE IS IMPORTANT

urlpatterns = [
    path("", views.job_list, name="list"),
    path("apply/<int:job_id>/", views.apply_job, name="apply"),
]

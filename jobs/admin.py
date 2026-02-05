from django.contrib import admin
from .models import Job, JobApplication


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location")
    search_fields = ("title", "company")


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("user", "job", "status", "applied_at")
    list_filter = ("status", "applied_at")
    search_fields = ("user__username", "job__title")

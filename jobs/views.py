from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, JobApplication
from profiles.models import Profile
from django.contrib import messages
from django.db.models import Q


def job_list(request):
    query = request.GET.get("q", "")
    location = request.GET.get("location", "")

    all_jobs = Job.objects.all()

    # SEARCH FILTER
    if query:
        all_jobs = all_jobs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    if location:
        all_jobs = all_jobs.filter(location__icontains=location)

    recommended_jobs = []
    applied_jobs = []
    profile = None
    completion = 0

    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()

        applied_jobs = request.user.jobapplication_set.values_list(
            "job_id", flat=True
        )

        # PROFILE COMPLETION
        if profile:
            completion = profile.completion_percentage

        # SKILL-BASED RECOMMENDATION
        if profile and profile.skills:
            skills = [s.strip().lower() for s in profile.skills.split(",")]

            for job in all_jobs:
                text = f"{job.title} {job.description}".lower()
                if any(skill in text for skill in skills):
                    recommended_jobs.append(job)

    return render(request, "jobs/job_list.html", {
        "jobs": all_jobs,
        "recommended_jobs": recommended_jobs,
        "applied_jobs": applied_jobs,
        "profile": profile,
        "completion": completion,
        "query": query,
        "location": location,
    })


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    profile = Profile.objects.get(user=request.user)

    if profile.completion_percentage < 100:
        messages.error(request, "Complete your profile before applying")
        return redirect("profiles:setup")

    JobApplication.objects.get_or_create(
        user=request.user,
        job=job
    )

    messages.success(request, "Application submitted successfully")

    return redirect("jobs:list")   # ✅ FIXED


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile
from training.models import CourseEnrollment


@login_required
def profile_setup(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.full_name = request.POST.get("full_name")
        profile.phone = request.POST.get("phone")
        experience = request.POST.get("experience")
        profile.experience = int(experience) if experience else None
        profile.location = request.POST.get("location")
        profile.skills = request.POST.get("skills")

        if request.FILES.get("resume"):
            profile.resume = request.FILES["resume"]

        profile.save()
        messages.success(request, "Profile saved successfully ✅")
        return redirect("dashboard:user")

    return render(request, "profiles/profile_setup.html", {"profile": profile})

@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)

    certificates = CourseEnrollment.objects.filter(
        user=request.user,
        completed=True
    )

    skills_list = []
    if profile.skills:
        skills_list = [s.strip() for s in profile.skills.split(",")]

    return render(request, "profiles/profile.html", {
        "profile": profile,
        "certificates": certificates,
        "skills_list": skills_list,
        "completion_percent": profile.completion_percentage
    })

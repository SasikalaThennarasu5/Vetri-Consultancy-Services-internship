from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    experience = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    skills = models.TextField(blank=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    @property
    def completion_percentage(self):
        fields = [
            self.full_name,
            self.phone,
            self.experience,
            self.location,
            self.skills,
            self.resume,
        ]

        completed = sum(
            1 for field in fields if field not in [None, "", 0]
        )

        return int((completed / len(fields)) * 100)

    # ✅ ADD THIS
    @property
    def profile_summary(self):
        parts = []

        if self.experience:
            parts.append(f"{self.experience} years experience")

        if self.skills:
            parts.append(f"Skilled in {self.skills}")

        if self.location:
            parts.append(f"Based in {self.location}")

        return " | ".join(parts)

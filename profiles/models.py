from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    experience = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    skills = models.TextField(blank=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    summary = models.TextField(
        blank=True,
        help_text="Short professional summary"
    )


    def completion_percentage(self):
        fields = [
            self.full_name,
            self.experience,
            self.location,
            self.skills,
            self.resume,
            self.summary,
        ]
        filled = sum(1 for f in fields if f)
        return int((filled / len(fields)) * 100)

    def __str__(self):
        return self.user.username

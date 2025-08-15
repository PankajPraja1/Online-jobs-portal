from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_employer = models.BooleanField(default=False)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    headline = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=100, blank=True)

class Job(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posted_jobs")
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=120, blank=True)
    min_experience = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    skills = models.CharField(max_length=512, blank=True, help_text="Comma separated skills")

    def __str__(self):
        return f"{self.title} - {self.employer.username}"

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    resume = models.FileField(upload_to="resumes/")
    cover_letter = models.TextField(blank=True)
    score = models.FloatField(null=True, blank=True)  # match score saved optionally
    created_at = models.DateTimeField(auto_now_add=True)

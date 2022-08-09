from django.db import models
from profiles.models import Counselor

# Create your models here.
class CounselorRequest(models.Model):
    email = models.EmailField()
    address = models.TextField()
    problem = models.TextField()
    assigned_counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return self.email
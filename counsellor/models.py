from django.db import models

# Create your models here.
class Councellor(models.Model):
    email = models.EmailField()
    address = models.TextField()
    problem = models.TextField()

    def __str__(self) -> str:
        return self.email
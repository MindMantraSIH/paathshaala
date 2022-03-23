from django.db import models
from autoslug import AutoSlugField
from profiles.models import School
from django.utils import timezone
from cloudinary.models import CloudinaryField
from profiles.models import User


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title', unique=True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    school = models.ForeignKey(School,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='feed/',null=True,blank=True)

    def __str__(self):
        return f'{self.school.user.name}: {self.title}' 

    upvote = models.ManyToManyField(User, related_name='like',blank=True)

    def number_of_upvotes(self):
        return self.upvote.count()
    

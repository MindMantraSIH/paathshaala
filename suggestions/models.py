from django.db import models
from autoslug import AutoSlugField
from profiles.models import School
from django.core.validators import MinValueValidator, MaxValueValidator


class Data(models.Model):
    # size = models.IntegerField(validators=[MinValueValidator(0),
    #                                    MaxValueValidator(5)])
    school = models.ForeignKey(School, on_delete=models.CASCADE, default=1)
    std = models.CharField(max_length=3)
    levelc = models.IntegerField()
    env = models.IntegerField()
    teachersc = models.IntegerField()
    prevdisc= models.IntegerField()
    fecilities = models.IntegerField()
    timetable = models.IntegerField()
    grpwork = models.IntegerField()
    mentalhlth = models.IntegerField()
    sportart=models.IntegerField()
    solveprob=models.IntegerField()
    creativecourse=models.IntegerField()
    foconindv=models.IntegerField()
    mannlearn=models.IntegerField()
    courserele=models.IntegerField()
    issuesofconc=models.IntegerField()
    aresolved=models.IntegerField()
    others = models.CharField(max_length=1000)
    #slug = AutoSlugField(populate_from='disc_title', unique=True)
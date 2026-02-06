from django.db import models


# Create your models here.
class aktier(models.Model):
    selskab = models.CharField(max_length=100)
    ticker = models.CharField(max_length=10)
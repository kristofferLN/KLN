from django.db import models


# Create your models here.
class aktier(models.Model):
    selskab = models.CharField(max_length=100)
    ticker = models.CharField(max_length=12)

    def __str__(self):
        return self.selskab
    
class aktiepriser(models.Model):
    selskab = models.ForeignKey(aktier, on_delete=models.CASCADE)
    dato = models.DateField()
    pris_close = models.FloatField()

    def __str__(self):
        return f"{self.selskab} - {self.dato} - {self.pris_close}"
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
    
class nyheder_links(models.Model):
    selskab = models.ForeignKey(aktier, on_delete=models.CASCADE)
    link = models.URLField()
    site = models.CharField(max_length=100)
    titel = models.CharField(max_length=200)
    tekst = models.TextField()

    def __str__(self):
        return f"{self.selskab} - {self.link}"
    
class ai_news_summary(models.Model):
    selskab = models.ForeignKey(aktier, on_delete=models.CASCADE)
    summary_text = models.TextField()
    nyheds_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.selskab} - {self.summary_text[:50]}..."
    
class annotation(models.Model):
    selskab = models.ForeignKey(aktier, on_delete=models.CASCADE)
    dato_fra = models.DateField()
    dato_til = models.DateField(blank=True, null=True)
    annotation_text = models.TextField()
    tidsperiode = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.selskab} - {self.dato_fra} to {self.dato_til} - {self.annotation_text[:50]}..."
    
class debat(models.Model):
    bruger = models.CharField(max_length=100)
    tekst = models.TextField()
    selskab = models.ManyToManyField(aktier)
    created_at = models.DateTimeField(auto_now_add=True)
    

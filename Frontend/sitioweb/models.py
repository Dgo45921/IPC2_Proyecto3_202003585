from django.db import models


# Create your models here.

class Respuesta(models.Model):
    texto = models.TextField()
    name = models.TextField(max_length=140)

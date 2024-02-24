from django.db import models

# Create your models here.
class Word_Map_Model(models.Model):
    keyword = models.CharField(max_length=100)
    response = models.CharField(max_length=100)

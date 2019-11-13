from django.db import models

# Create your models here.
class Photo(models.Model):
    image = models.ImageField(upload_to='photo')
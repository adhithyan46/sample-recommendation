from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tour(models.Model):
    name = models.CharField(max_length=100)
    locations = models.CharField(max_length=100)
    price = models.FloatField()
    description=models.FloatField()
    ImageURL = models.URLField()

    def __str__(self):
     return self.name

class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_loc = models.CharField(max_length=100)
    budget = models.FloatField()
    ImageURL = models.URLField()
    
    def __str__(self):
        return self.name
    
    
    
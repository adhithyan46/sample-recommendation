from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tour(models.Model):
    name = models.CharField(max_length=100)
    locations = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField() 
    # image_url = models.URLField()  
    image = models.ImageField(upload_to='tours/',default='')

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_loc = models.CharField(max_length=100)
    budget = models.FloatField()
    image_url = models.URLField(blank=True, null=True)  # Optional

    def __str__(self):
        return self.user.username  # Return username instead of name

    
    
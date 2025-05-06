from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    
    is_seller = models.BooleanField(default = False)
    is_buyer = models.BooleanField(default = False)
    image = models.URLField()
    full_name = models.CharField(max_length = 100)


class Buyer(models.Model):
    user = models.OneToOneField(
        "User", on_delete=models.CASCADE, primary_key = True)

    def __str__(self):
        return self.user.username



class Seller(models.Model):
    user = models.OneToOneField(
        "User", on_delete=models.CASCADE, primary_key=True)
    
    type = models.CharField(max_length = 50)
    street_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=5)

    logo = models.URLField() #gæti þurft ehv variable inní 
    bio = models.TextField()

    def __str__(self):
        return self.user.username


from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    
    is_seller = models.BooleanField(default = False)
    is_buyer = models.BooleanField(default = False)
    image = models.URLField()
    full_name = models.CharField(max_length = 100)

    def makeInits(self):
        print("makeInits")

    def __str__(self):
        #self.makeInits()
        names = self.full_name.split()
        inits = "".join([x[0] for x in names])
        return inits

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
        return "XX"

class Filter(models.Model):

    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=True, blank=True)
    
    monitor = models.BooleanField(default=False)
    name = models.CharField(max_length=50, null=True, blank=True)
    area = models.CharField(max_length=50, null=True, blank=True)
    price = models.CharField(max_length=50, null=True, blank=True)
    desc = models.CharField(max_length=50, null=True, blank=True)
    re_type = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Notification(models.Model):

    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=True, blank=True)

    property = models.ForeignKey(
        "real_estates.Property", on_delete=models.CASCADE, null=True, blank=True)

    offer = models.ForeignKey(
        "real_estates.Offer", on_delete=models.CASCADE, null=True, blank=True)

    count = models.IntegerField()

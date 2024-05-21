from django.db import models
from django.db.models.functions import Now
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Brand(models.Model):
    name = models.CharField(max_length=80)

class Category(models.Model):
    name = models.CharField(max_length=80)

class Model(models.Model):
    name = models.CharField(max_length=80)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class UAV(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    description = models.TextField()
    weight = models.FloatField()
    model = models.ForeignKey(Model,on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,  null=True)
    image = models.ImageField(upload_to="rentalProject/static")
    hourly_price = models.FloatField(help_text="TRY")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def image_link(self):
        return "https://erenalkan.com/" + self.image_path




class Rent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    uav = models.ForeignKey(UAV, on_delete=models.CASCADE, null=False)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    price = models.FloatField(help_text="TRY")


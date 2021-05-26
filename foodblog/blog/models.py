from django.db import models
from django.contrib.auth.models import User
# Create your models here.

		

class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name

class Food(models.Model):
    # user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=False, blank=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    ingredients = models.CharField(max_length=500, null=False, blank=False)
    short_description = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
from django.db import models

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100)

class News(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    time = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


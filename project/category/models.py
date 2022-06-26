from django.db import models
# from shop.models import Product
# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name
class Domains(models.Model):
    Domain_name = models.CharField(max_length=30)
    Category = models.ForeignKey(Category, on_delete = models.CASCADE)

    def __str__(self):
        return self.Domain_name

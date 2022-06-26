from django.db import models
from category.models import Category, Domains
from user.models import User
# from shop.models import Product
# Create your models here.

class Qualification(models.Model):
    Qualification_name = models.CharField(max_length=30)

    def __str__(self):
        return self.Qualification_name

class Mentor(models.Model):
    mentor_price = models.FloatField(null=True, blank=True,)
    mentor_desc = models.CharField(max_length=250, null=True,)
    date_created = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    Cat=models.ForeignKey(Category,on_delete = models.CASCADE,null=True, blank=True,)
    Qual= models.ForeignKey(Qualification,on_delete = models.CASCADE,null=True, blank=True,)
    Dom= models.ForeignKey(Domains,on_delete = models.CASCADE,null=True, blank=True,)
    mentoruser=models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True,)
    mentor_image = models.ImageField(null=True, blank=True, upload_to='')



    # Category = models.ForeignKey(Category, on_delete = models.CASCADE)

    
    def get_price(self):
        return self.mentor_price    


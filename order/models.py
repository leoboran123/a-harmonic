from django.db import models
from django.contrib.auth.models import User

from product.models import Product, Category

# Create your models here.

class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.product.title


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.title

    @property
    def price(self):
        return (self.product.price)
    
    @property
    def amount(self):
        return (self.quantity * self.product.price)
    

class Coupon(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length = 50, blank=True)
    discount = models.FloatField()
    code = models.CharField(max_length = 30, editable=False)


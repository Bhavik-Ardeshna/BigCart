from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=20,unique=True)
    slug = AutoSlugField(populate_from='name')
    image = models.ImageField(upload_to='categories',blank=True,null=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name_plural = 'Categories'

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=30,unique=True)
    slug = AutoSlugField(populate_from='name')
    image = models.ImageField(upload_to='product')
    brand = models.CharField(max_length=30)
    product_detail = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=15,decimal_places=2,default=0.0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ratings =  models.IntegerField(default=10,validators=[MaxValueValidator(10),MinValueValidator(1)])
    review = models.CharField(blank=True,max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.review



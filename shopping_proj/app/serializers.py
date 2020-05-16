from rest_framework import serializers
from . import models

class ProductSerialize(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['category','name','slug','image','product_detail']
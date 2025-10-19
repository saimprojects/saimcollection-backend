from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "slug", "description", "price", "file", "is_active", "external_link",]
        read_only_fields = ["id", "slug"]

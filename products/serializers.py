from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "title", "slug", "description", "price", "file", "is_active", "external_link"]
        read_only_fields = ["id", "slug"]

    def get_file(self, obj):
        if obj.file:
            # agar Cloudinary use ho raha hai, full URL Cloudinary ke domain ke sath return kare
            if str(obj.file).startswith("http"):
                return obj.file
            return f"https://res.cloudinary.com/dxommxt6d/{obj.file}"
        return None

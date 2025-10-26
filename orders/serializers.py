from rest_framework import serializers
from .models import Order, DownloadLink
from products.models import Product
from products.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    product_title = serializers.CharField(source="product.title", read_only=True)
    product_slug = serializers.CharField(source="product.slug", read_only=True)

    download_link = serializers.SerializerMethodField()
    external_link = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "product",
            "product_id",
            "product_title",
            "product_slug",
            "user",
            "status",
            "approved_at",
            "download_link",
            "external_link",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "approved_at", "user"]

    def get_download_link(self, obj: Order):
        link = getattr(obj, "download_link", None)
        if not link:
            return None

        if link.is_valid() and not link.external_warning:
            remaining = max(link.max_downloads - link.download_count, 0)
            return {
                "id": str(link.id),
                "expires_at": link.expires_at,
                "remaining_downloads": remaining,
                "external_warning": link.external_warning,
            }
        return None

    def get_external_link(self, obj: Order):
        link = getattr(obj, "download_link", None)
        if link and link.external_warning:
            return link.url
        return None


class CreateOrderSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product'
    )

    class Meta:
        model = Order
        fields = ["product_id"]

    def create(self, validated_data):
        user = self.context["request"].user
        product = validated_data.pop("product")  # pop product to avoid passing twice

        # avoid duplicate active orders for same product
        existing_order = Order.objects.filter(user=user, product=product, status="pending").first()
        if existing_order:
            return existing_order

        return Order.objects.create(user=user, product=product)

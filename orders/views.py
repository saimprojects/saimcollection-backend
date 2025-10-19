from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product
from .models import Order, DownloadLink
from .serializers import OrderSerializer, CreateOrderSerializer


# -----------------------------
# Admin / General Views
# -----------------------------

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user_id=self.kwargs['user_id']).order_by('-created_at')


# -----------------------------
# User-Specific Views
# -----------------------------

class CreateOrderView(generics.CreateAPIView):
    serializer_class = CreateOrderSerializer
    permission_classes = [permissions.IsAuthenticated]


class MyOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")


class DownloadLinkView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, link_id):
        link = get_object_or_404(DownloadLink, id=link_id, order__user=request.user)
        if not link.is_valid():
            return Response(
                {"detail": "Link expired or download limit reached"},
                status=status.HTTP_410_GONE
            )
        link.register_download()
        return redirect(link.url)

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


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if not user_id:
            return Order.objects.none()
        return Order.objects.filter(user_id=user_id).order_by('-created_at')


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
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


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
        if not link.url:
            return Response({"detail": "Download URL not found"}, status=status.HTTP_404_NOT_FOUND)

        return redirect(link.url)


#------------------------------
#payment system
#--------------------------------

# views.py me add karo

class SubmitPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        transaction_id = request.data.get("transaction_id")

        if not transaction_id:
            return Response({"detail": "Transaction ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        order.transaction_id = transaction_id
        order.status = Order.STATUS_PENDING  # ya STATUS_APPROVED agar auto approve karna hai
        order.save()

        return Response({"detail": "Payment submitted successfully!", "id": str(order.id)}, status=status.HTTP_200_OK)

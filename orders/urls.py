from django.urls import path
from .views import (
    OrderListCreateView,
    OrderDetailView,
    UserOrdersView,
    CreateOrderView,
    MyOrdersView,
    DownloadLinkView,
    SubmitPaymentView
)

urlpatterns = [
    # User-specific views
    path("", MyOrdersView.as_view(), name="my_orders"),
    path("create/", CreateOrderView.as_view(), name="create_order"),
    path("download/<uuid:link_id>/", DownloadLinkView.as_view(), name="download_link"),

    # General admin / list views
    path("all/", OrderListCreateView.as_view(), name="order-list-create"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("user/<int:user_id>/", UserOrdersView.as_view(), name="user-orders"),
        path("<uuid:order_id>/submit-payment/", SubmitPaymentView.as_view(), name="submit_payment"),

]

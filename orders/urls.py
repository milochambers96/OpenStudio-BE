from django.urls import path
from .views.admin_view import AllOrdersView
from .views.buyer_views import PurchaseRequestsListView, CreateOrderView, CancelOrderView, ProcessDummyPaymentView
from .views.seller_views import SellerOrdersListView, SpecificOrderView, ReviewOrderView, OrderShippedView
from .views.counterparties_views import UnviewedOrdersView, MarkOrdersViewedView

urlpatterns = [
    path('all/', AllOrdersView.as_view(), name='admin-orders-list-view'),
    
    path('purchase-requests/', PurchaseRequestsListView.as_view(), name='buyer-requests-view'),
    path('create/', CreateOrderView.as_view(), name='create-order-request-view'),
    path('cancel/<int:order_id>', CancelOrderView.as_view(), name='cancel-order-view'),
    path('payment/<int:order_id>', ProcessDummyPaymentView.as_view(), name='process-payment-view'),
    
    path('seller/', SellerOrdersListView.as_view(), name='seller-orders'),
    path('order-details/<int:order_id>', SpecificOrderView.as_view(), name='order-details'),
    path('review/<int:order_id>', ReviewOrderView.as_view(), name='review-order-view'),
    path('shipped/<int:order_id>', OrderShippedView.as_view(), name="order-shipped"),

    path('unviewed-orders/', UnviewedOrdersView.as_view(), name='order-notifcations-view'),
    path('mark-viewed/', MarkOrdersViewedView.as_view(), name='mark-orders-viewed')
]


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated

from ..models import Order
from ..serializer import OrderSerializer
        
class SellerOrdersListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request): 
        try:
            orders_list = Order.objects.get(seller = request.user)
            seralized_orders = OrderSerializer(orders_list)
            return Response(seralized_orders.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            raise NotFound(detail = 'Order list not found.')

class SpecificOrderView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, order_id):
        try: 
            order = Order.objects.get(pk=order_id)
            serialized_order = OrderSerializer(order)
            if order.seller == request.user:
                return Response(serialized_order.data, status=status.HTTP_200_OK)
            else:
                return PermissionDenied()
        except Order.DoesNotExist:
            raise NotFound(detail = 'Order not found.')
    
class ReviewOrderView(APIView):
    permission_classes = (IsAuthenticated, )

    def patch(self, request, order_id):
        try: 
            order = Order.objects.get(pk=order_id, seller=request.user)
        except Order.DoesNotExist:
            raise NotFound(detail='Order not found.')
        
        order_action = request.data.get('action')
        if order_action == 'accept':
            order.status='accepted'
            order.save()
            return Response({'message': 'Order accepted'}, status=status.HTTP_200_OK)
        elif order_action == 'cancel':
            order.status == 'cancelled'
            order.save()
            return Response({'message': 'Order cancelled'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid order action'}, status=status.HTTP_400_BAD_REQUEST)

class OrderShippedView(APIView):
    permission_classes = (IsAuthenticated, )

    def patch(self, request, order_id):
        try: 
            order = Order.objects.get(pk=order_id, seller=request.user)
        except Order.DoesNotExist:
            raise NotFound(detail="Order not found.")
        
        if order.status != 'ready_to_ship':
            return Response({'error': 'Order is not ready to ship.'}, status=status.HTTP_400_BAD_REQUEST)

        order.status='shipped'
        order.save()
        return Response({'message': 'Order status updated to shipped.'}, status=status.HTTP_200_OK)


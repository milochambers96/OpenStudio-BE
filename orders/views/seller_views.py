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
        purchase_requests = Order.objects.filter(seller=request.user)
        if not purchase_requests.exists():
            return Response({'detail': 'No purchase requests found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serialized_purchases = OrderSerializer(purchase_requests, many=True)
        return Response(serialized_purchases.data, status=status.HTTP_200_OK)

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
    permission_classes = (IsAuthenticated,)

    def patch(self, request, order_id):
        try: 
            order = Order.objects.get(pk=order_id, seller=request.user)
        except Order.DoesNotExist:
            raise NotFound(detail='Order not found.')
        
        order_action = request.data.get('action')
        if order_action == 'accept':
            order.status = 'accepted'
            order.save()
            return Response({'message': 'Order accepted', 'status': order.status}, status=status.HTTP_200_OK)
        elif order_action == 'cancel':
            order.status = 'cancelled'  
            order.save()
            return Response({'message': 'Order cancelled', 'status': order.status}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid order action'}, status=status.HTTP_400_BAD_REQUEST)
        

class OrderShippedView(APIView):
    permission_classes = (IsAuthenticated, )

    def patch(self, request, order_id):
        try: 
            order = Order.objects.get(pk=order_id, seller=request.user)
        except Order.DoesNotExist:
            raise NotFound(detail="Order not found.")
        
        if order.status != 'ready to ship':
            return Response({'error': 'Order is not ready to ship.'}, status=status.HTTP_400_BAD_REQUEST)

        order.status = 'shipped'
        order.save()
        return Response({'message': 'Order status updated to shipped.'}, status=status.HTTP_200_OK)


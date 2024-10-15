from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


from ..models import Order
from artworks.models import Artwork
from ..serializer import OrderSerializer

class PurchaseRequestsListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get (self, request):
        purchase_requests = Order.objects.filter(buyer=request.user)
        if not purchase_requests.exists():
            return Response({'detail': 'No purchase requests found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serialized_purchases = OrderSerializer(purchase_requests, many=True)
        return Response(serialized_purchases.data, status=status.HTTP_200_OK)


class CreateOrderView(APIView):
    permission_classes = (IsAuthenticated, )

    def post (self, request): 
        buyer = request.user
        artwork_id = request.data.get('artwork_id')
        try:
            artwork = Artwork.objects.get(pk=artwork_id)
        except Artwork.DoesNotExist:
            raise NotFound(detail="Artwork not found.")
         
        seller = artwork.artist 

        final_price = request.data.get('final_price')
    
        order_data = {
            'buyer': buyer.id, 
            'seller': seller.id,
            'artwork': artwork.id,
            'price': final_price,
            'status': 'pending',
        }

        serialized_order = OrderSerializer(data=order_data)

        try:
        
            if serialized_order.is_valid():
                serialized_order.save()
                return Response(serialized_order.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serialized_order.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error: 
            print('Error')
            return Response(error.__dict__ if error.__dict__ else str(error), status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        

class CancelOrderView(APIView):
    permission_classes = (IsAuthenticated, )

    def patch(self, request, order_id):
        try: 
            order = Order.objects.get(pk=order_id, buyer=request.user)
        except Order.DoesNotExist:
            raise NotFound(detail="Order not found")
        
        if order.status not in ['pending', 'accepted']:
            return Response({'error': 'This order cannot be cancelled'}, status=status.HTTP_400_BAD_REQUEST)
        order.status = 'cancelled'
        order.viewed_by_seller = False
        order.save()

        serialized_order = OrderSerializer(order)
        return Response(serialized_order.data, status=status.HTTP_200_OK)        
        

class ProcessDummyPaymentView(APIView):
    permission_classes = (IsAuthenticated,)

    #! transactions ensures all the actions happen at once across DBs 
    @transaction.atomic
    def patch(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id, buyer=request.user)

        if order.status != 'accepted':
            return Response({'error': 'Order is not accepted yet.'}, status=status.HTTP_400_BAD_REQUEST)

        # Dummy Payment Logic as a placeholder would need stripe or something similar in the real world.
        payment_successful = True

        if payment_successful:
            order.status = 'ready to ship'
            order.viewed_by_seller = False
            order.save()

            artwork = order.artwork
            artwork.quantity_for_sale -= 1
            if artwork.quantity_for_sale <= 0:
                artwork.is_for_sale = False
                artwork.quantity_for_sale = 0 
            artwork.save()

            return Response({
                'message': 'Payment successful, order is ready to ship.',
                'new_quantity': artwork.quantity_for_sale,
                'is_for_sale': artwork.is_for_sale
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Payment failed.'}, status=status.HTTP_400_BAD_REQUEST)
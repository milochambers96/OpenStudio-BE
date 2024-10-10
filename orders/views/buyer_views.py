from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from ..models import Order
from artworks.models import Artwork
from ..serializer import OrderSerializer

class PurchaseRequestsListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get (self, request):
        try: 
            purchase_requests = Order.objects.get(buyer = request.user)
            serialized_purchases = OrderSerializer(purchase_requests)
            return Response(serialized_purchases.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            raise NotFound(detail = 'Purchase requests not found.')
        
class CreateOrderView(APIView):
    permission_classes = (IsAuthenticated, )

    def post (self, request): 
        buyer = request.user
        artwork_id = request.data.get('artwork.id')
        try:
            artwork = Artwork.objects.get(pk=artwork_id)
        except Artwork.DoesNotExist:
            raise NotFound(detail="Artwork not found.")
         
        seller = artwork.artist 

        ##! This will be caculated on the frontend
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

class ProcessDummyPaymentView(APIView):
    permission_classes = (IsAuthenticated, )

    def patch(self, request, order_id):
        try: 
            order = Order.objects.get(pk=order_id, buyer=request.user) 
        except Order.DoesNotExist:
            raise NotFound(detail='Order not found.')

        if order.status != 'accepted':
            return Response({'error': 'Order is not accepted yet.'}, status=status.HTTP_400_BAD_REQUEST)

        ##! Dummy Payment Logic as a placeholder was student project purpose
        payment_successful = True

        if payment_successful:
            order.status = 'ready_to_ship'
            order.save()

            return Response({'message': 'Payment successful, order is ready to ship.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Payment failed.'}, status=status.HTTP_400_BAD_REQUEST)

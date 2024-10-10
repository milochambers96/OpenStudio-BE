from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAdminUser

from ..models import Order
from ..serializer import OrderSerializer

class AllOrdersView(APIView):
    permission_classes = (IsAdminUser, )

    def get(self, _request):
        try: 
            orders = Order.objects.all()
            serialized_orders = OrderSerializer(orders)
            return Response(serialized_orders.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            raise PermissionDenied()

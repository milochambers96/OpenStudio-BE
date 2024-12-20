from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..models import Order


class UnviewedOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        has_unviewed_orders = False

        try:
            if user.user_type == 'collector':
                has_unviewed_orders = Order.objects.filter(buyer=user, viewed_by_buyer=False).exists()
            elif user.user_type == 'artist':
                has_unviewed_orders = Order.objects.filter(seller=user, viewed_by_seller=False).exists()
            else:
                return Response({"error": "Invalid user type"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"has_unviewed_orders": has_unviewed_orders})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MarkOrdersViewedView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user_type = request.data.get('user_type')

        if user_type not in ['artist', 'collector']:
            return Response({"error": "Invalid user type"}, status=status.HTTP_400_BAD_REQUEST)

        if user_type == 'artist':
            Order.objects.filter(seller=user, viewed_by_seller=False).update(viewed_by_seller=True)
        elif user_type == 'collector':
            Order.objects.filter(buyer=user, viewed_by_buyer=False).update(viewed_by_buyer=True)

        return Response({"message": "Orders marked as viewed"}, status=status.HTTP_200_OK)
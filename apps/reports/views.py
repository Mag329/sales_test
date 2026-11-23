
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .services import build_sales_table


class SalesTableAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = build_sales_table()
        return Response(data)

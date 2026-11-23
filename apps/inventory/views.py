
from decimal import Decimal

from django.db.models import Sum, Count
from django.db.models.functions import Coalesce

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Warehouse, Inventory
from .serializers import (
    WarehouseSerializer,
    InventorySerializer,
    InventorySummarySerializer,
)
from .filters import InventoryFilter
from .pagination import InventoryPagination


class WarehouseListView(generics.ListAPIView):
    queryset = Warehouse.objects.all().order_by("id")
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]


class WarehouseDetailView(generics.RetrieveAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]


class InventoryListView(generics.ListAPIView):
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]

    pagination_class = InventoryPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]

    filterset_class = InventoryFilter

    ordering_fields = [
        "quantity_t",
        "reserved_t",
        "product__name",
        "warehouse__name",
    ]

    ordering = [
        "product_id",
        "warehouse_id",
    ]

    def get_queryset(self):
        return (
            Inventory.objects
            .select_related("product", "warehouse")
            .all()
        )


class InventoryDetailView(generics.RetrieveAPIView):
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        from django.shortcuts import get_object_or_404

        return get_object_or_404(
            Inventory.objects.select_related(
                "product", "warehouse"
            ),
            product_id=self.kwargs["product_id"],
            warehouse_id=self.kwargs["warehouse_id"],
        )


class InventorySummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Inventory.objects.all()

        warehouse_id = request.query_params.get(
            "warehouse_id"
        )
        product_id = request.query_params.get(
            "product_id"
        )

        if warehouse_id:
            queryset = queryset.filter(
                warehouse_id=warehouse_id
            )

        if product_id:
            queryset = queryset.filter(
                product_id=product_id
            )

        aggregates = queryset.aggregate(
            total_quantity_t=Coalesce(
                Sum("quantity_t"),
                Decimal("0"),
            ),
            total_reserved_t=Coalesce(
                Sum("reserved_t"),
                Decimal("0"),
            ),
            warehouses_count=Count(
                "warehouse_id",
                distinct=True,
            ),
            products_count=Count(
                "product_id",
                distinct=True,
            ),
        )

        aggregates["total_available_t"] = (
            aggregates["total_quantity_t"]
            - aggregates["total_reserved_t"]
        )

        serializer = InventorySummarySerializer(aggregates)
        return Response(serializer.data)

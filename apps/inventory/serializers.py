
from rest_framework import serializers

from .models import Warehouse, Inventory


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = (
            "id",
            "name",
        )


class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
    )
    warehouse_name = serializers.CharField(
        source="warehouse.name",
        read_only=True,
    )
    available_t = serializers.SerializerMethodField()

    class Meta:
        model = Inventory
        fields = (
            "product",
            "product_name",
            "warehouse",
            "warehouse_name",
            "quantity_t",
            "reserved_t",
            "available_t",
        )

    def get_available_t(self, obj):
        return obj.quantity_t - obj.reserved_t


class InventorySummarySerializer(serializers.Serializer):
    total_quantity_t = serializers.DecimalField(
        max_digits=20,
        decimal_places=3,
    )
    total_reserved_t = serializers.DecimalField(
        max_digits=20,
        decimal_places=3,
    )
    total_available_t = serializers.DecimalField(
        max_digits=20,
        decimal_places=3,
    )
    warehouses_count = serializers.IntegerField()
    products_count = serializers.IntegerField()

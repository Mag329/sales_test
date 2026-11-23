
from django.urls import path

from .views import (
    WarehouseListView,
    WarehouseDetailView,
    InventoryListView,
    InventoryDetailView,
    InventorySummaryView,
)


app_name = "inventory"

urlpatterns = [
    path(
        "warehouses/",
        WarehouseListView.as_view(),
        name="warehouse-list",
    ),
    path(
        "warehouses/<int:pk>/",
        WarehouseDetailView.as_view(),
        name="warehouse-detail",
    ),
    path(
        "summary/",
        InventorySummaryView.as_view(),
        name="inventory-summary",
    ),
    path(
        "<int:product_id>/<int:warehouse_id>/",
        InventoryDetailView.as_view(),
        name="inventory-detail",
    ),
    path(
        "",
        InventoryListView.as_view(),
        name="inventory-list",
    ),
]

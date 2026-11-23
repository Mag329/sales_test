
from decimal import Decimal

import django_filters
from django.db.models import F

from apps.catalog.models import Category
from .models import Inventory


class InventoryFilter(django_filters.FilterSet):
    warehouse_id = django_filters.NumberFilter(
        field_name="warehouse_id",
    )
    product_id = django_filters.NumberFilter(
        field_name="product_id",
    )

    category_id = django_filters.NumberFilter(
        method="filter_category",
    )
    include_children = django_filters.BooleanFilter(
        method="filter_noop",
    )

    quantity_min = django_filters.NumberFilter(
        field_name="quantity_t",
        lookup_expr="gte",
    )
    quantity_max = django_filters.NumberFilter(
        field_name="quantity_t",
        lookup_expr="lte",
    )

    reserved_min = django_filters.NumberFilter(
        field_name="reserved_t",
        lookup_expr="gte",
    )
    reserved_max = django_filters.NumberFilter(
        field_name="reserved_t",
        lookup_expr="lte",
    )

    available_only = django_filters.BooleanFilter(
        method="filter_available",
    )

    search = django_filters.CharFilter(
        field_name="product__name",
        lookup_expr="icontains",
    )

    class Meta:
        model = Inventory
        fields = []

    def filter_noop(self, queryset, name, value):
        return queryset

    def filter_category(self, queryset, name, value):
        category_id = int(value)

        include_children = (
            self.form.cleaned_data.get(
                "include_children", False
            )
        )

        if not include_children:
            return queryset.filter(
                product__category_id=category_id
            )

        categories = list(
            Category.objects.values("id", "parent_id")
        )

        children_map = {}

        for category in categories:
            parent_id = category["parent_id"]

            children_map.setdefault(
                parent_id, []
            ).append(category["id"])

        category_ids = set()
        stack = [category_id]

        while stack:
            current_id = stack.pop()

            if current_id in category_ids:
                continue

            category_ids.add(current_id)

            stack.extend(
                children_map.get(current_id, [])
            )

        return queryset.filter(
            product__category_id__in=category_ids
        )

    def filter_available(self, queryset, name, value):
        if value:
            return queryset.filter(
                quantity_t__gt=F("reserved_t")
            )

        return queryset

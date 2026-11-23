from rest_framework import serializers
from django.utils.html import escape
import logging
from .models import Category, Product

logger = logging.getLogger(__name__)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "parent", "name", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
    
    def validate_name(self, value):
        if not value.strip():
            logger.warning("Empty name provided for Category")
            raise serializers.ValidationError("Наименование не может быть пустым.")
        return escape(value.strip())
    

class CategoryCreateSerializer(CategorySerializer):
    pass


class CategoryUpdateSerializer(CategorySerializer):
    class Meta:
        model = Category
        fields = (
            "name",
            "parent",
        )

    def validate_parent(self, parent):
        instance = self.instance

        if instance is None or parent is None:
            return parent

        if parent.pk == instance.pk:
            raise serializers.ValidationError(
                "Категория не может быть родителем самой себе."
            )

        current = parent
        visited = set()

        while current is not None:
            if current.pk == instance.pk:
                raise serializers.ValidationError(
                    "Нельзя переместить категорию "
                    "внутрь её дочерней категории."
                )

            if current.pk in visited:
                raise serializers.ValidationError(
                    "В иерархии категорий обнаружен цикл."
                )

            visited.add(current.pk)
            current = current.parent

        return parent
    

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "category_name",
            "name",
            "origin_country",
            "package_kg",
            "cost_rub_kg",
            "min_price_rub_kg",
            "created_at",
            "updated_at",
        )


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "name",
            "origin_country",
            "package_kg",
            "cost_rub_kg",
            "min_price_rub_kg",
        )

    def validate(self, attrs):
        if attrs["min_price_rub_kg"] < attrs["cost_rub_kg"]:
            raise serializers.ValidationError({
                "min_price_rub_kg": (
                    "Минимальная цена не может быть "
                    "ниже себестоимости."
                )
            })
        return attrs


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "category",
            "name",
            "origin_country",
            "package_kg",
            "cost_rub_kg",
            "min_price_rub_kg",
        )

    def validate(self, attrs):
        instance = self.instance

        cost = attrs.get(
            "cost_rub_kg",
            instance.cost_rub_kg,
        )
        price = attrs.get(
            "min_price_rub_kg",
            instance.min_price_rub_kg,
        )

        if price < cost:
            raise serializers.ValidationError({
                "min_price_rub_kg": (
                    "Минимальная цена не может быть "
                    "ниже себестоимости."
                )
            })

        return attrs

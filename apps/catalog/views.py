from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Category, Product
from .serializers import (
    CategorySerializer,
    CategoryCreateSerializer,
    CategoryUpdateSerializer,
    ProductSerializer,
    ProductCreateSerializer,
    ProductUpdateSerializer,
)
import logging

from .permissions import StrictModelPermissions


logger = logging.getLogger(__name__)

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    permission_classes = [StrictModelPermissions]
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CategoryCreateSerializer
        return CategorySerializer
    
    def perform_create(self, serializer):
        instance = serializer.save()

        logger.info(
            "CREATE /categories/%s | user=%s",
            instance.pk,
            self.request.user.pk,
        )
    
    
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.select_related("parent").all()
    permission_classes = [StrictModelPermissions]

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return CategoryUpdateSerializer
        return CategorySerializer

    def perform_update(self, serializer):
        instance = serializer.save()

        logger.info(
            "UPDATE /categories/%s | user=%s",
            instance.pk,
            self.request.user.pk,
        )

    def perform_destroy(self, instance):
        category_id = instance.pk
        instance.delete()

        logger.info(
            "DELETE /categories/%s | user=%s",
            category_id,
            self.request.user.pk,
        )
    

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.select_related(
        "category"
    ).all()

    permission_classes = [StrictModelPermissions]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductCreateSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        instance = serializer.save()

        logger.info(
            "CREATE /products/%s | user=%s",
            instance.pk,
            self.request.user.pk,
        )


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related(
        "category"
    ).all()

    permission_classes = [StrictModelPermissions]

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return ProductUpdateSerializer
        return ProductSerializer

    def perform_update(self, serializer):
        instance = serializer.save()

        logger.info(
            "UPDATE /products/%s | user=%s",
            instance.pk,
            self.request.user.pk,
        )

    def perform_destroy(self, instance):
        product_id = instance.pk
        instance.delete()

        logger.info(
            "DELETE /products/%s | user=%s",
            product_id,
            self.request.user.pk,
        )

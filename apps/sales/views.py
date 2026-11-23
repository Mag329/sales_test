from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
# from .models import Currency, CurrencyType, Event
# from .serializers import (
#     CurrencySerializer, 
#     CurrencyCreateSerializer, 
#     CurrencyUpdateSerializer,
#     CurrencyTypeSerializer,
#     CurrencyTypeCreateSerializer,
#     CurrencyTypeUpdateSerializer,
#     EventCreateSerializer,
#     EventSerializer,
#     EventUpdateSerializer
# )
import logging

from .permissions import StrictModelPermissions


logger = logging.getLogger(__name__)

class CurrencyListCreateView(generics.ListCreateAPIView):
    # queryset = Currency.objects.all()
    # permission_classes = [StrictModelPermissions]
    
    # def get_serializer_class(self):
    #     if self.request.method == "POST":
    #         return CurrencyCreateSerializer
    #     return CurrencySerializer
    
    def get(self, request, *args, **kwargs):
        logger.info(f"GET /currencies | user={request.user}")
        return super().get(request, *args, **kwargs)
    
    
class CurrencyDetailView(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Currency.objects.all()
    # permission_classes = [StrictModelPermissions]
    
    # def get_serializer_class(self):
    #     if self.request.method in ["PUT", "PATCH"]:
    #         return CurrencyUpdateSerializer
    #     return CurrencySerializer
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        logger.info(f"UPDATE /currencies/{instance.id} | user={request.user}")
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        logger.warning(f"UPDATE /currencies/{instance.id} failed | errors={serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.info(f"DELETE /currencies/{instance.id} | user={request.user}")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# class CurrencyTypeListCreateView(generics.ListCreateAPIView):
#     queryset = CurrencyType.objects.all()
#     permission_classes = [StrictModelPermissions]
    
#     def get_serializer_class(self):
#         if self.request.method == "POST":
#             return CurrencyTypeCreateSerializer
#         return CurrencyTypeSerializer
    
class CurrencyTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    # queryset = CurrencyType.objects.all()
    # permission_classes = [StrictModelPermissions]
    
    # def get_serializer_class(self):
    #     if self.request.method in ["PUT", "PATCH"]:
    #         return CurrencyTypeUpdateSerializer
    #     return CurrencyTypeSerializer
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        logger.info(f"UPDATE /currency-types/{instance.id} | user={request.user}")
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        logger.warning(f"UPDATE /currency-types/{instance.id} failed | errors={serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.info(f"DELETE /currency-types/{instance.id} | user={request.user}")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# class EventListCreateView(generics.ListCreateAPIView):
#     queryset = Event.objects.all()
#     permission_classes = [StrictModelPermissions]
#     parser_classes = [MultiPartParser, FormParser]
    
#     def get_serializer_class(self):
#         if self.request.method == "POST":
#             return EventCreateSerializer
#         return EventSerializer
    
    
class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Event.objects.all()
    # permission_classes = [StrictModelPermissions]
    # parser_classes = [MultiPartParser, FormParser]
    
    # def get_serializer_class(self):
    #     if self.request.method in ["PUT", "PATCH"]:
    #         return EventUpdateSerializer
    #     return EventSerializer
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.info(f"UPDATE /events/{instance.id} | user={request.user}")
            return Response(serializer.data)
        logger.warning(f"UPDATE /events/{instance.id} failed | errors={serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        logger.info(f"DELETE /events/{instance.id} | user={request.user}")
        return Response(status=status.HTTP_204_NO_CONTENT)
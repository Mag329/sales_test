from rest_framework import serializers
from django.utils.html import escape
import logging
# from .models import Currency, CurrencyType, Event

logger = logging.getLogger(__name__)


# class CurrencySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Currency
#         fields = ("id", "mnemonic", "name", "created_at", "updated_at")
#         read_only_fields = ("id", "created_at", "updated_at")
        
#     def validate_mnemonic(self, value):
#         if not value.isalpha() or len(value) != 3:
#             logger.warning(f"Invalid mnemonic format: {value}")
#             raise serializers.ValidationError("Мнемоника должна состоять из 3 буквенных символов.")
#         return escape(value.upper())
    
#     def validate_name(self, value):
#         if not value.strip():
#             logger.warning("Empty name provided for Currency")
#             raise serializers.ValidationError("Наименование не может быть пустым.")
#         return escape(value.strip())
    
#     def validate(self, attrs):
#         mnemonic = attrs.get('mnemonic')
        
#         if mnemonic is None:
#             return attrs
        
#         if Currency.objects.filter(mnemonic=mnemonic.upper()).exists():
#             logger.warning(f"Duplicate mnemonic attempt: {mnemonic}")
#             raise serializers.ValidationError("Мнемоника уже существует.")
#         logger.info(f"Currency validation passed for mnemonic: {mnemonic}")
#         return attrs
    

# class CurrencyCreateSerializer(CurrencySerializer):
#     pass


# class CurrencyUpdateSerializer(CurrencySerializer):
#     mnemonic = serializers.CharField(required=False)
#     name = serializers.CharField(required=False)
    

# class CurrencyTypeSerializer(serializers.ModelSerializer):
#     currency = serializers.PrimaryKeyRelatedField(
#         queryset=Currency.objects.all()
#     )
    
#     class Meta:
#         model = CurrencyType
#         fields = "__all__"
#         read_only_fields = ("id", "created_at", "updated_at")
        

# class CurrencyTypeCreateSerializer(CurrencyTypeSerializer):
#     pass

# class CurrencyTypeUpdateSerializer(CurrencyTypeSerializer):
#     currency = serializers.PrimaryKeyRelatedField(
#         queryset=Currency.objects.all(),
#         required=False
#     )
#     name = serializers.CharField(required=False)
#     region = serializers.CharField(required=False)
#     active = serializers.BooleanField(required=False)
    
    
# class EventSerializer(serializers.ModelSerializer):
#     currency_type = serializers.PrimaryKeyRelatedField(
#         queryset=CurrencyType.objects.all()
#     )
    
#     class Meta:
#         model = Event
#         fields = "__all__"
#         read_only_fields = ("id", "created_at", "updated_at")
        
    
# class EventCreateSerializer(EventSerializer):
#     pass


# class EventUpdateSerializer(EventSerializer):
#     currency_type = serializers.PrimaryKeyRelatedField(
#         queryset=CurrencyType.objects.all(),
#         required=False
#     )
#     timestamp = serializers.DateTimeField(required=False)
#     value = serializers.DecimalField(max_digits=20, decimal_places=4, required=False)
#     description = serializers.CharField(required=False, allow_blank=True)
    
#     def validate_value(self, value):
#         if value < 0:
#             logger.warning(f"Negative event value provided: {value}")
#             raise serializers.ValidationError("Значение не может быть отрицательным.")
#         return value
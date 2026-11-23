from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer, 
    TokenRefreshSerializer,
    TokenVerifySerializer,
    TokenBlacklistSerializer,
)
from rest_framework_simplejwt.exceptions import InvalidToken

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": "Неверный логин или пароль."
    }

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        try:
            return super().validate(attrs)
        except InvalidToken:
            raise InvalidToken("Предоставленный refresh-токен недействителен или его срок действия истек.")

class CustomTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        try:
            return super().validate(attrs)
        except InvalidToken:
            raise InvalidToken("Токен недействителен, изменен или его срок действия истек.")
        
class CustomTokenBlacklistSerializer(TokenBlacklistSerializer):
    def validate(self, attrs):
        try:
            return super().validate(attrs)
        except InvalidToken:
            raise InvalidToken("Невозможно отозвать токен: он недействителен или уже находится в черном списке.")
        

# admin.py

from django.contrib import admin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

# Переименовываем
OutstandingToken._meta.verbose_name = "Токен"
OutstandingToken._meta.verbose_name_plural = "Токены"

BlacklistedToken._meta.verbose_name = "Заблокированный токен"
BlacklistedToken._meta.verbose_name_plural = "Заблокированные токены"

# Перерегистрируем
admin.site.unregister(OutstandingToken)
admin.site.unregister(BlacklistedToken)

@admin.register(OutstandingToken)
class OutstandingTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "jti", "created_at", "expires_at")


@admin.register(BlacklistedToken)
class BlacklistedTokenAdmin(admin.ModelAdmin):
    list_display = ("token", "blacklisted_at")
    
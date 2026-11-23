from django.contrib import admin

# from .models import Currency, CurrencyType, Event


# @admin.register(Currency)
# class CurrencyAdmin(admin.ModelAdmin):
#     list_display = ("mnemonic", "name")
#     search_fields = ("mnemonic", "name")
#     ordering = ("mnemonic",)
#     readonly_fields = ("created_at", "updated_at")
    
#     fieldsets = (
#         ('Основная информация', {
#             'fields': ('mnemonic', 'name')
#         }),
#         ('Дополнительная информация', {
#             'fields': ('created_at', 'updated_at')
#         }),
#     )
    
    
# @admin.register(CurrencyType)
# class CurrencyTypeAdmin(admin.ModelAdmin):
#     list_display = ("name", "region", "currency", 'active')
#     search_fields = ("name", "region", "currency__mnemonic")
#     ordering = ("name",)
#     readonly_fields = ("created_at", "updated_at")
#     list_editable = ('active',)
    
#     fieldsets = (
#         ('Основная информация', {
#             'fields': ('currency', 'name', 'region', 'active')
#         }),
#         ('Дополнительная информация', {
#             'fields': ('created_at', 'updated_at')
#         }),
#     )
    

# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
#     list_display = ("currency_type", "timestamp", "value")
#     search_fields = ("currency_type__name", "currency_type__region", "currency_type__currency__mnemonic")
#     ordering = ("-timestamp",)
#     readonly_fields = ("created_at", "updated_at")
    
#     fieldsets = (
#         ('Основная информация', {
#             'fields': ('currency_type', 'timestamp', 'value')
#         }),
#         ('Вложение', {
#             'fields': ('file',)
#         }),
#         ('Дополнительная информация', {
#             'fields': ('created_at', 'updated_at')
#         }),
#     )
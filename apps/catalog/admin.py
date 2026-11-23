from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "parent_name",
        "children_count",
        "products_count",
    )

    list_display_links = ("id", "name")

    search_fields = (
        "name",
        "parent__name",
    )

    ordering = ("name",)

    readonly_fields = (
        "parent_name",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = ("parent",)

    list_select_related = ("parent",)

    fieldsets = (
        ("Основная информация", {
            "fields": (
                "name",
                "parent",
                "parent_name",
            ),
        }),
        ("Дополнительная информация", {
            "fields": (
                "created_at",
                "updated_at",
            ),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Родительская категория")
    def parent_name(self, obj):
        if not obj or not obj.parent_id:
            return "—"
        return obj.parent.name

    @admin.display(description="Подкатегорий")
    def children_count(self, obj):
        return obj.children.count()

    @admin.display(description="Товаров")
    def products_count(self, obj):
        return obj.products.count()
    
    
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
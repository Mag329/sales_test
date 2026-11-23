from django.urls import path

from .views import CategoryListCreateView, CategoryDetailView, ProductListCreateView, ProductDetailView

app_name = 'catalog'

# urlpatterns = [
#     path('currencies/', CurrencyListCreateView.as_view(), name='currency-list-create'),
#     path('currencies/<int:pk>/', CurrencyDetailView.as_view(), name='currency-detail'),
#     path('currency-types/', CurrencyTypeListCreateView.as_view(), name='currency-type-list-create'),
#     path('currency-types/<int:pk>/', CurrencyTypeDetailView.as_view(), name='currency-type-detail'),
#     path('events/', EventListCreateView.as_view(), name='event-list-create'),
#     path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
# ]

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]
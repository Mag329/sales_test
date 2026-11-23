from django.urls import path
from .views import CurrencyListCreateView

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
    path('currencies/', CurrencyListCreateView.as_view(), name='currency-list-create'),
]
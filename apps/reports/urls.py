
from django.urls import path

from .views import SalesTableAPIView


urlpatterns = [
    path(
        "sales-table/",
        SalesTableAPIView.as_view(),
        name="sales-table",
    ),
]

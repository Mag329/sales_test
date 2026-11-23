from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from health_check.views import HealthCheckView


schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Currency API",
        default_version='v1',
        description="API для управления валютами, их типами и событиями"
    ),
    public=True,
    permission_classes=(AllowAny,),
)    

admin.site.site_title = "W051-currency admin"
admin.site.site_header = "Админ панель W051-currency"
admin.site.index_title = "Админ панель W051-currency"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include([
        path("", include("apps.catalog.urls")),
        path("inventory/", include("apps.inventory.urls")),
        path("reports/", include("apps.reports.urls")),
    ])),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path(
        "health/",
        HealthCheckView.as_view(
            checks=[  # optional, default is all but 3rd party checks
                "health_check.Database",
                # 3rd party checks
                "health_check.contrib.psutil.Disk",
                "health_check.contrib.psutil.Memory",
            ],
        ),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.ENABLE_SWAGGER:
    urlpatterns += [
        path(
            "api/v1/swagger/",
            schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'
        ),
    ]

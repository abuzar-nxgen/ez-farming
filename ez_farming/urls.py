"""
URL configuration for ez_farming project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from ezcore.views import home_view  # adjust import as needed
from ezdairy.views import dairy_view
from ezmeat.views import meat_view
from ezanimal.views import animal_view
from ezcore.health_and_feed.views import haf_view
from ezcore.inventory_and_sales.views import ias_view




schema_view = get_schema_view(
   openapi.Info(
      title="EZ Farming API",
      default_version='v1',
      description="API for EZ Farming Livestock Management System",
      terms_of_service="https://www.ezfarming.com/terms/",
      contact=openapi.Contact(email="contact@ezfarming.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/', include('ez_farming.api_urls')),
    path('accounts/', include('allauth.urls')),
    
    # API documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', home_view),  # <-- this handles the empty path "/"
    path('ezdairy/', dairy_view),
    path('ezmeat/', meat_view),
    path('ezanimal/', animal_view), 
    path('ezcore/haf/', haf_view), 
    path('ezcore/ias/', ias_view), 
]

# Add i18n patterns for internationalization
# urlpatterns += i18n_patterns(
#     # Add any URLs that need to be translated here
# )

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

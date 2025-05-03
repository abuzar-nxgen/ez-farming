from django.urls import path, include
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('animal/', include('ezanimal.urls')),
    path('dairy/', include('ezdairy.urls')),
    path('meat/', include('ezmeat.urls')),
    path('core/', include('ezcore.urls')),
]

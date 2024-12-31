"""
URL configuration for real_estate_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from api.views import (
                        ProjectsViewSet,
                        HousesViewSet,
                        SectionsViewSet,
                        FlatsViewSet, bulk_update_flats,
                        login
)

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Real Estate API",
      default_version='v1',
      description="API for real estate management",
   ),
   public=True,
   permission_classes=[permissions.AllowAny]
)

router = DefaultRouter()
router.register(r'project', ProjectsViewSet, basename='project')
router.register(r'house', HousesViewSet, basename='house')
router.register(r'section', SectionsViewSet, basename='section')
router.register(r'flat', FlatsViewSet, basename='flat')

urlpatterns = [
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
   path('', include(router.urls)),
   path('flat/', bulk_update_flats, name='bulk-update-flats'),
   path('login/', login, name='login'),
]

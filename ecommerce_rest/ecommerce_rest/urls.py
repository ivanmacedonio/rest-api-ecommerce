
from django.contrib import admin
from django.urls import path, include, re_path
from apps.users.views import Login, Logout
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.static import serve
from django.conf import settings

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



schema_view = get_schema_view(
   openapi.Info(
      title="Documentacion de API",
      default_version='v0.1',
      description="Documentacion publica de API de mi ecommerce",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="ivanmacedonio778@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

#---URLS GENERALES
urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', Logout.as_view(), name='Logout'),
    path('products/', include('apps.products.api.serializers.routers')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('login/', Login.as_view(),name='Login'),
    #path('refresh-token/', UserToken.as_view(),name='refresh-token'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', include('apps.users.api.routers')),

]
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]

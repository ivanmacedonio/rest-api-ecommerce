from rest_framework.routers import DefaultRouter

from apps.users.api.api import UserViewSet

router = DefaultRouter()

router.register('', UserViewSet, basename="users" )

urlpatterns = router.urls

#una vez creado el router lo enlazamos con el archivo de rutas principales 

#path('usuario/', include('apps.users.api.routers')),


from rest_framework.routers import DefaultRouter
from apps.products.api.serializers.views.products_views import ProductViewSet
from apps.products.api.serializers.views.general_views import *
#importamos un router y el viewset que se le va a asignar 

router = DefaultRouter() #creamos el router 

router.register(r'products', ProductViewSet, basename='products') #registramos la url correspondiente a la viewset 
router.register(r'measure_unit', MeasureUnitViewSet, basename='measure_unit') #registramos la url correspondiente a la viewset 
router.register(r'indicators', IndicatorViewSet, basename='indicators') #registramos la url correspondiente a la viewset 
router.register(r'category_products', CategoryProductViewSet, basename='category_products') #registramos la url correspondiente a la viewset 

urlpatterns = router.urls #lo agregamos a urlpatterns para que django lo encuentre a la hora de escribir la url


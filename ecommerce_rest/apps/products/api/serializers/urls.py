from django.urls import path
from apps.products.api.serializers.views.general_views import MeasureUnitListApiView, IndicatorListApiView,CategoryProductListApiView
from apps.products.api.serializers.views.products_views import  ProductCreateListAPIView, ProductRetrieveAPIView
#----URLS DE LAS LISTAS 
urlpatterns = [
    
    
    path('product/', ProductCreateListAPIView.as_view(), name= 'product'),
    path('product/retrieve/<int:pk>/', ProductRetrieveAPIView.as_view(), name= 'product_retrieve'),
]

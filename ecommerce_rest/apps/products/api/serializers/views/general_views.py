from rest_framework import viewsets
from apps.base.api import GeneralListApiView
from apps.products.api.serializers.general_serializers import MeasureUnitSerializer, IndicatorSerializer, CategoryProductSerializer
from django.shortcuts import render

class MeasureUnitViewSet(viewsets.ModelViewSet):

    serializer_class = MeasureUnitSerializer


'''
Los viewsets tienen una vista de la cual podemos o asignarles un template o 
podemos extraer informacion. Los campos que se definen en el viewset son el backend 
del Crud, en la pestaña donde se definen, es decir, en .viewsets les asignamos 
un serializador para que a la hora de renderizar informacion puedan devolverla 
en formato clave valor, es decir JSON 
'''



class IndicatorViewSet(viewsets.ModelViewSet):

    serializer_class = IndicatorSerializer



class CategoryProductViewSet(viewsets.ModelViewSet):

    serializer_class = CategoryProductSerializer


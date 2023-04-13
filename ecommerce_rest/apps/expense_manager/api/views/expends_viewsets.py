from django.models.db import Q
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from apps.expense_manager.api.serializers.expense_serializer import *
from rest_framework.decorators import action
from apps.expense_manager.models import Supplier
from apps.expense_manager.api.serializers.general_serializer import SupplierSerializer


class ExpenseViewSet(viewsets.GenericViewSet):

    serializer_class = ExpenseSerializer 

    @action(methods=['get'], detail=False) #creamos una funcion para el generic viewset 
    #la cual va a buscar al proveedor
    def search_supplier(self,request):
        ruc_or_bisness_name = request.query_params.get('ruc_or_business_name', '')
        #esta variable guarda o la razon social o el nombre del negocio 
        supplier = Supplier.objects.filter(
        Q(ruc__iexact=ruc_or_bisness_name) |
        Q(business_name__iexact=ruc_or_bisness_name)).first()

        if supplier:
            supplier_serializer = SupplierSerializer(supplier)
            return Response(supplier_serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    



        

        #busca por razon social o nombre de negocio, si existe alguno, toma 
        #el primero que encuentre, y lo serializa.











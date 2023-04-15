from django.models.db import Q
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from apps.expense_manager.api.serializers.expense_serializer import *
from rest_framework.decorators import action
from apps.expense_manager.models import Supplier, Voucher, PaymentType
from apps.expense_manager.api.serializers.general_serializer import *
from apps.products.models import Product
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.base.utils import format_date

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
    #Funcion que registra el proveedor
    @action(methods=['post'], detail=False)
    def new_supplier(self,request):
        data_supplier = request.data
        data_supplier = SupplierRegisterSerializer(data_supplier)
        if data_supplier.is_valid():
            data_supplier = data_supplier.save()
            return Response ({'message': 'Proveedor registrado correctamente!',
                              'supplier': data_supplier.data},status=status.HTTP_201_CREATED)
        return Response ({'error': data_supplier.errors}, status=status.HTTP_400_BAD_REQUEST)
   #se encarga de traer datos como producto y voucher a la lista desplegable del formulario de crear factura 
    @action(methods=['get'], detail= False)
    def get_vouchers(self,request):
        data = Voucher.objects.filter(state=True).order_by('id')
        data = VoucherSerializer(data, many=True).data
        return Response(data)
    
    @action(methods=['get'], detail= False)
    def get_payment_type(self,request):
        data = PaymentType.objects.filter(state=True).order_by('id')
        data = PaymentTypeSerializer(data, many=True).data
        return Response(data)

    @action(methods=['get'], detail= False)
    def get_products(self,request):
        data = Product.objects.filter(state=True).order_by('id')
        data = ProductSerializer(data, many=True).data
        return Response(data) 
    
    #encargado de crear las facturas 

    def create(self,request):
        data = request.data

        #decode del token que devuelve el usuario y su token
        JWT_authenticator = JWTAuthentication
        user, _ = JWT_authenticator.authenticate(request)
        data['user'] = user.id

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Factura registrada correctamente'}, status=status.HTTP_201_CREATED)
        else: 
            return Response({'message': 'Ocurrieron errores'})
            
#saber que usuario esta haciendo la creacion, extrayendo del token el usuario



    def format_data(self,data):
        data['date'] = format_date(data['date'])
        return data

        









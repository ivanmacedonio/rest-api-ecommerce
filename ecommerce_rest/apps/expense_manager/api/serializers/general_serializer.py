from rest_framework import serializers
from apps.expense_manager.models import *
from apps.products.models import Product

class SupplierSerializer(serializers.ModelSerializer):

    class Meta:

        model = Supplier

        fields = ('id','ruc', 'business_name', 'adress')


class VoucherSerializer(serializers.ModelSerializer):

    class Meta:

        model = Voucher

        fields = ('id','name')


class PaymentTypeSerializer(serializers.ModelSerializer):

    class Meta:

        model = Voucher

        fields = ('id','name')

class ProductSerializer(serializers.ModelSerializer):

    class Meta:

        model = Product
        fields = ('id', 'name')
        

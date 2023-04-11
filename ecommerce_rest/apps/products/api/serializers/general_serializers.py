from apps.products.models import MeasureUnit, CategoryProduct, Indicator
from rest_framework import serializers


class MeasureUnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeasureUnit
        exclude = ('state','created_date', 'modified_date', 'deleted_date') #excluido xq en el listado no lo quiero ver 

class CategoryProductSerializer(serializers.ModelSerializer):

    class Meta:
        model= CategoryProduct
        exclude = ('state','created_date', 'modified_date', 'deleted_date')

class IndicatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Indicator
        exclude = ('state','created_date', 'modified_date', 'deleted_date')



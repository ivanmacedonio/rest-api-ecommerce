from rest_framework import serializers
from apps.products.models import Product
from apps.products.api.serializers.general_serializers import MeasureUnitSerializer, CategoryProductSerializer

class ProductSerializer(serializers.ModelSerializer):

    class Meta:

        model = Product
        exclude = ('state','created_date', 'modified_date', 'deleted_date')

    def validate_measure_unit(self,value):
        if value == '' or value == None:
            raise serializers.ValidationError('Debes ingresar la MU')
        return value
    
    def validate_category_product(self,value):
        if value == '' or value == None:
            raise serializers.ValidationError('Debe ingresar una categoria')
        return value
    
    def validate(self,data):
        if 'measure_unit' not in data.keys():
            raise serializers.ValidationError("Debe ingresar una unidad de medida")
        
        if 'category_product' not in data.keys():
            raise serializers.ValidationError("Debe ingresar una categoria")
        
        return data

    def to_representation(self, instance):
        return{

            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'image': instance.image.url if instance.image != '' else '', #la toma en cuenta si la instancia es diferente de texto, texto es lo que devuelve cuando no hay nada en el campo img
            'measure_unit': instance.measure_unit.description if instance.measure_unit is not None else '',
            'category_product': instance.category_product.description if instance.category_product is not None else '',
        }

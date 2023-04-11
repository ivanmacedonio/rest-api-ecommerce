from django.db import models
from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel

class MeasureUnit(BaseModel):

    description=  models.CharField('Descripcion', max_length=50, blank=False, null=False, unique= True)
    historical= HistoricalRecords()

    #funcionalidades del Historical records 

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value



    class Meta:

        verbose_name= 'Unidad de Medida'

        verbose_name_plural= 'Unidades de Medidas'

    def __str__(self):

        return self.description

class CategoryProduct(BaseModel):

    description= models.CharField('Descripcion', max_length=50, unique=True, null=False, blank=False)
    historical= HistoricalRecords()

    #funcionalidades del Historical records 

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta:

        verbose_name= 'Categoria de Producto'
        verbose_name_plural=  'Categorias de Productos'

    def __str__(self):

        return self.description

class Indicator(BaseModel):

    category_product= models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, verbose_name='Indicador de Oferta')
    descount_value= models.PositiveSmallIntegerField(default= 0)
    historical= HistoricalRecords()

    #funcionalidades del Historical records 

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta:

        verbose_name= 'Indicador de Oferta'

        verbose_name_plural = 'Indicadores de Ofertas'

    def __str__(self):

        return f'Oferta de la categoria {self.category_product}: {self.descount_value}% '
    
class Product(BaseModel):

    name=models.CharField('Nombre de Producto', max_length=150, unique=True, null=False, blank=False)
    description= models.TextField('Descripcion de Producto', blank=False, null=False)
    image= models.ImageField('Imagen del Producto', upload_to='products/', blank=True, null=True)
    measure_unit= models.ForeignKey(MeasureUnit, on_delete=models.CASCADE, verbose_name='Unidad de Medida', null=True)
    category_product= models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, null=True,verbose_name= 'Categoria de Producto')
    historical= HistoricalRecords()

    #funcionalidades del Historical records 

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta:

        verbose_name= 'Producto'

        verbose_name_plural = 'Productos'

    def __str__(self):

        return self.name









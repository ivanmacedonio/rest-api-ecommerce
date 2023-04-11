from apps.products.api.serializers.product_serializers import ProductSerializer
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from apps.users.authentication_mixins import Authentication

class ProductViewSet(Authentication, viewsets.ModelViewSet):

    serializer_class = ProductSerializer

    def get_queryset(self, pk=None):
        if pk is None: #si no se envia pk hace get de todo, si devuelve el get donde coincida la id con la pk
            return self.get_serializer().Meta.model.objects.filter(state=True)
        return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()

    def post(self,request): #creamos un post nosotros mismos 
        serializer = self.serializer_class(data=request.data) #en una variable guardamos el serializador 
        if serializer.is_valid(): #si pasa los requerimientos de los campos
            serializer.save()#lo guarda en la bbd (lista y retrieve)
            return Response ({'message': 'Product created Succesfully!'})
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk=None):
        product= self.get_queryset().filter(id=pk).first() #en una variable guardamos
    #la consulta que filtre por el id que busquemos. si estamos en producto 1 y el id 
    #coincide con un producto existente, sigue abajo
        if product: #si existio el producto
            product.state = False #lo desactiva
            product.save() #lo guarda 
            return Response({'message': 'Product Deleted Succesfully!'}, status= status.HTTP_200_OK)
        return Response({'error': 'No existe un producto'},status = status.HTTP_400_BAD_REQUEST)

    def create (self,request): 

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Producto creado correctamente!'}, status= status.HTTP_201_CREATED)
        return Response (serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def update(self,request,pk=None):
        if self.get_queryset(pk):
            product_serializer = self.serializer_class(self.get_queryset(pk), data= request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(product_serializer.data, status= status.HTTP_200_OK)
            return Response(product_serializer.errors, status= status.HTTP_400_BAD_REQUEST)


    
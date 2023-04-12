from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from apps.users.models import User
from rest_framework.decorators import action
from apps.users.api.serializers import UserSerializer, UserListSerializer, UpdateUserSerializer, PasswordSerializer

class UserViewSet(viewsets.GenericViewSet): #genericviewset es un tipo de viewset no basado en un modelo el cual contiene los 
    #metodos de get object y getqueryset, que espera que sobreescribamos los metodos,sino no los muestra
    model = User

    serializer_class = UserSerializer

    list_serializer_class = UserListSerializer

    queryset = None #si existe, sobreescribe el none, si no existe queda el None

    #debemos definir las rutas de CRUD para que las utilice...

    def get_object(self,pk): #recibe un pk y basado en ese pk traer el objeto relacionado, si no lo encuentra que tire raise
        return get_object_or_404(self.model, pk=pk)
    #si encuentra la pk dentro de model que coincida con la pk que le llega lo devuelve
    #sino retorna 404

        

    def get_queryset(self):
        if self.queryset is None: #si el metodo ya existia el none se sobreescribe, si no existe en genericviewset queda el none y lo creamos nosotros
            self.queryset = self.model.objects.filter(is_active= True).values('id', 'username', 'email', 'name')
        #hace un filtro de los usuarios que estan activos y lo guarda en la vriable de la viewset e indicamos que valores mostrar
        #en values solo pueden incluirse valores que ya hayamos asignado al serializador (to representation), pues no podemos incluir un value no serializado!!!
        return self.queryset #si ya estaba definida que la devuelva como vino de origen
    
    @action(detail=True, methods=['post']) #detail true indica que recibira un condicional, en este caso el id.
    #el method indica de que manera va a trabajar la informacion
    def set_password(self,request,pk=None): #se encarga de cambiar la contraseña
        user = self.get_object(pk) #guardamos el usuario que va a ejecutar la query
        password_serializer = PasswordSerializer(data=request.data) #serializa el password con el que llega por request
        if password_serializer.is_valid(): #si es valido / paso las validaciones del serializer creado recientemente
            user.set_password(password_serializer.validated_data['password']) #el password del usuario cambia por el password que llego por request
            user.save()#lo guarda en la bbdd
            return Response({
                'message': 'Contraseña actualizada correctamente!'
            })
        return Response({
            'message': 'Error en la informacion enviada'
        })


    def list(self,request): #serializamos los objectos para mostrarlos
        users= self.get_queryset() #se carga la consulta de los usuarios activos en users
        users_serializer = self.list_serializer_class(users, many=True) #serializa la data almacenada en users y la guarda en users_serializers
        return Response(users_serializer.data, status=status.HTTP_200_OK) #retorna la data ya serializada 

    def create(self,request):

        user_serializer = self.serializer_class(data=request.data) #se serializa la data que llega por request
        if user_serializer.is_valid():#si es valida
            user_serializer.save()#guarda la data en la bbdd
            return Response({'message': 'Usuario creado correctamente!'}, status=status.HTTP_201_CREATED)
        return Response ({'message': 'No se pudo crear el usuario!', 'errors': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request, pk=None): #pk none inicializa la variable pk
        user= self.get_object(pk) #get_object busca un objeto que tenga una id dentro del model que coincida con la que recibio , 
        #y la que coincida guarda los datos dentro de user
        user_serializer= self.serializer_class(user)#serializa la data de user 
        return Response(user_serializer.data)#la retorna en json
    
    def update(self,request,pk=None):
        user = self.get_object(pk)#traemos el objeto
        user_serializer = UpdateUserSerializer(user, data=request.data) #serializamos el objeto y la data de user se cambia por la que llega mediante request
        if user_serializer.is_valid(): #si es valido
            user_serializer.save() #lo actualiza
            return Response ({
                'message': 'Usuario actualizado correctamente'
            }, status=status.HTTP_200_OK)
        return Response({'message': 'Hay errores en el update!'}, status=status.HTTP_400_BAD_REQUEST)
    

#como el user serializer class es un serializador que usamos para todo, tiene campos obligatorios que 
#obstruyen en la actualizacion, pues en el update no enviamos todos los datos, sino los que 
#queremos actualizar, obstruye q el serializador general pide password. creamos un nuevo serializador

    def destroy(self,request,pk=None):
        user_destroy = self.model.objects.filter(id=pk).update(is_active=False)
#donde la id coincida desactiva el usuario. la funcion update devuelve la cantidad de registros afectados
#si el registro afectado fue 1, significa que el usuario fue deleteado 
        if user_destroy == 1: #si es 1 significa que un registro fue updateado o ""eliminado"""
            return Response({'message': 'Usuario eliminado correctamente'})
        return Response({'message': 'No se encontro el id correspondiente'}, status=status.HTTP_404_NOT_FOUND)



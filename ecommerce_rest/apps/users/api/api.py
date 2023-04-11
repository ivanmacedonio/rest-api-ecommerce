from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from apps.users.models import User
from rest_framework.decorators import api_view
from apps.users.api.serializers import UserSerializer, UserListSerializer

@api_view(['GET', 'POST']) #carga como parametros validos el get y post
def userApiView(request):

    if request.method == 'GET': #si el metodo es get

        users = User.objects.all().values('id', 'username', 'email', 'password') #en users se guarda toda la informacion, esta informacion es el modelo user cargado con su variable objects

        users_serializer = UserSerializer(users, many=True) #carga en los campos del serializador (los mismos campos que el modelo) la informacion que recolecto users 
         
        return Response(users_serializer.data, status= status.HTTP_200_OK)  #retorna la informacion serializada de users
    
    elif request.method == 'POST': #si el metodo http es post 

        user_serializer = UserSerializer(data = request.data) #consulta si los datos ingresados por el ususario coinciden con las variables del modelo
        
        if user_serializer.is_valid(): #si coinciden 

            user_serializer.save() #se guarda el usuario cargado de la informacion que llego por post en la bbdd 

            return Response(user_serializer.data,status=status.HTTP_201_CREATED) #retorna los datos que se guardaron en la variable user_serializer 
        
        return Response(user_serializer.errors) #en caso de no coincidir se envia la variable errors que indica cual es el problema 

#toda la informacion enviada por POST se va a guardar en una variable
#llamada request, donde se almacena especificamente en la parte de data

'''
20. UserSerializer tiene las variables del modelo y compara el nombre de 
sus variables (data) con la data enviada por el usuario recibida por post
(request.data). Es decir, des-serializa la data para compararla con 
la que esta entrando por metodo http

si la informacion coincide, guarda el usuario en la base de datos
y los datos que envia a la bbdd son la data de la variable creada
(recordemos que la variable creada es user_serializer y la data
que contiene es la que post le envio )

'''

@api_view(['GET', 'PUT', 'DELETE']) #usamos el metodo get y put para obtener un dato 
def user_detail_view(request , pk): #la funcion toma como parametro pk que simula ser una id 
    if request.method == 'GET': #si el metodo es get 
        user = User.objects.filter(id=pk).first() #en user se guarda la info del ususario que coincida con la id que llego por parametro
        user_serializer = UserSerializer(user) #convertimos en json los datos del usuario 
        return Response(user_serializer.data, status=status.HTTP_200_OK) #retorna los datos 
        
    elif request.method == 'PUT': #si el metodo es put va a hacer un update de la informacion
        user = User.objects.filter(id=pk).first()
        user_serializer = UserSerializer(user,data= request.data, context= request.data) #la data del user va a remplazarse por la data que llego por request (es decir la data que trajo el PUT)
        #el context le da la capacidad de acceder a las instancias estando definidas en otro lado 
        if user_serializer.is_valid(): #si coincidieron las id y paso del renglon 55
            user_serializer.save() #guarda la variable en la bbdd (la remplaza)
            return Response(user_serializer.data, status=status.HTTP_200_OK) #guarda la data en la bbdd
        return Response(user_serializer.errors,status=status.HTTP_400_BAD_REQUEST) #si no pasa del 55 hubo un error, entonces retorna error

    elif request.method == 'DELETE':
        user = User.objects.filter(id=pk).first()
        user.delete()
        return Response({'message':'User Deleted suscessfuly!'}, status=status.HTTP_200_OK)


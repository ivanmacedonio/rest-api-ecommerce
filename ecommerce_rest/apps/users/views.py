from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.contrib.sessions.models import Session
from rest_framework.views import APIView
from apps.users.api.serializers import CustomTokenObtainPairSerializer
from django.contrib.auth import authenticate
from apps.users.api.serializers import CustomUserSerializer
from rest_framework.generics import GenericAPIView
from apps.users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView


class Login(TokenObtainPairView): #clase para login que hereda esa clase de la lib

    serializer_class = CustomTokenObtainPairSerializer #serializador del logueo definido en users.api.serializers 

    
    def post(self,request,*args,**kwargs): #como funciona la informacion que llega por post, es decir, los datos del usuario
        username = request.data.get('username','') #en username se guarda la informacion que cae por request
        password = request.data.get('password','')#lo mismo que en username
        user= authenticate( #si existen los campos devuelve un true 
            username = username,
            password = password,
        )

        if user: #si devolvio un true, es decir los datos son validos
            login_serializer = self.serializer_class(data=request.data) #serializador del login 
            if login_serializer.is_valid(): #si la data serializada es valida
                user_serializer = CustomUserSerializer(user) #en user se guardan sus datos
                return Response ({ #e indicamos 
                    'token' : login_serializer.validated_data.get('access'), #que su token tiene acceso
                    'refresh-token': login_serializer.validated_data.get('refresh'), #le activamos el refresh a su token
                    'user': user_serializer.data, #la variable usuario relacionada a su token va a valer como el usuario que cayo por request data
                    'message': 'Inicio de sesion Exitoso!' #mensaje 
                }, status= status.HTTP_200_OK)
            return Response({'error': 'Contraseña o username incorrecto'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Contraseña o username incorrecto'},status=status.HTTP_400_BAD_REQUEST)

class Logout(GenericAPIView):
    def post (self,request,*args,**kwargs):
        user = User.objects.filter(id=request.data.get('user', 0)) #recibe un usuario por parametro el cual coincida su id con la que llego por request
                    #en caso de no encontrar un user del cual tomar la id, toma la ID 0 indicando que no existe el user
        if user.exists(): #si la id del usuario coincide con una registrada en la bbdd
            RefreshToken.for_user(user.first()) #el usuario que recibe le vuelve a generar un token, al ser nuevo y no coincidir con el anterior que uso durante su sesion, lo bota del sistema
            return Response({'message': 'Sesion cerrada correctamente'},status=status.HTTP_200_OK)
        return Response({'error': 'No existe este usuario!'},status=status.HTTP_400_BAD_REQUEST)

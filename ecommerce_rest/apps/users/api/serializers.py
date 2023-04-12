from rest_framework import serializers
from apps.users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass

class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = ('username', 'email', 'name', 'last_name')


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = '__all__'

    def create(self, validated_data): #encriptar la pass al crear un usuario
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        updated_user= super().update(instance,validated_data) #como no sabemos cuantos campos recibimos, super se encarga de tomar todos los que envien aunque no sepamos cuantos llegan para actualizar 
        updated_user.set_password(validated_data['password']) #setea el password en la variable password almacenada en validated data
        updated_user.save()
        return updated_user

class UserListSerializer(serializers.ModelSerializer):

    class Meta:

        model= User

    def to_representation(self, instance):
        #data= super().to_representation(instance) #le guardamos a una variable todos los mdatos recibidos de la instancia 
        #print(data) #devuelve las instancias, es decir, los campos del model User cargados
        return {
            'id': instance['id'],
            'name': instance['name'],
            'username': instance['username'],
            'email': instance['email'],
            
        }

#podemos cambiar los nombres que aparecen en pantalla 

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'last_name')


class PasswordSerializer(serializers.Serializer):#.SERIALIZER porque no debe ser basado en un modelo, simplemente serializa la info
    password = serializers.CharField(max_length = 128, min_length= 6, write_only = True)
    password2 = serializers.CharField(max_length = 128, min_length= 6, write_only = True)

    def validate(self,data):
        if data['password'] != data['password2']: #si la data de pass1 es diferente a pass2
            raise serializers.ValidationError('Debe ingresar ambas contraseñas iguales') #error
        return data #sino la retorna serializada!
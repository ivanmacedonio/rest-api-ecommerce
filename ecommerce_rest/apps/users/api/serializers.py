from rest_framework import serializers
from apps.users.models import User



class UserTokenSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields= ('username', 'email')

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
            'username': instance['username'],
            'email': instance['email'],
            'password': instance['password'],
        }

#podemos cambiar los nombres que aparecen en pantalla 


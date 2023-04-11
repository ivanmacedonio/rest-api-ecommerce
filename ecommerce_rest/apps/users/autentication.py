from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from datetime import timedelta
from django.utils import timezone
from django.conf import settings





class ExpiringTokenAuthentication(TokenAuthentication): 
    expired = False

    def expires_in(self,token): #calcula el tiempo de expiracion del token
        time_elapsed=  timezone.now()  - token.created #cuanto tiempo transcurrio desde la creacion del token
        left_time= timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed #tiempo restante
        return left_time #retorna el tiempo restante

    def is_token_expired(self,token): #indica si el token expiro o no
        return self.expires_in(token) <  timedelta(seconds=0) #si el tiempo restante es menor a 0 significa que expiro, le añade la logica a la funcion anterior
    
    def token_expire_handler(self,token):#crea una variable para saber si expiro el token y desencadena un codigo que verifica si ya expiro el token o no, llamando a la funcion que realiza el calculo
        is_expire = self.is_token_expired(token) #guarda un true o false dependiendo si vencio o no
        if is_expire:#si es true
            self.expired = True
            user = token.user
            token.delete()
            token = self.get_model().objects.create(user=token.user)
        
        return is_expire,token


    def authenticate_credentials(self, key): #key se refiere  a token, la funcion se encarga de guardar el token de la currentsession  
        message,user,token = None,None,None #por defecto valen none, si no se les carga ningun dato xq no existia el token no tira error
        try: #ejecuta a no ser que 
            token = self.get_model().objects.select_related('user').get(key=key)  #el get model hacia la clase tokenauth importa el modelo de token donde coincida el usuario y token
            user = token.user
        except self.get_model().DoesNotExist: #el token no exista
            message= 'Token invalido!'
            self.expired = True
            
        if token is not None:
            if not token.user.is_active: #si el usuario esta inactivo o ban
                message= 'Usuario no activo o eliminado!'
            
        
        
            is_expired = self.token_expire_handler(token) #guarda true o false dependiendo de si expiro o no
            if  is_expired: #si expiro
                message= 'Token expirado!'
        
        
        return (user,token,message,self.expired) #retorna el token y usuario, el mensaje depende 
    #del if al que haya entrado
  
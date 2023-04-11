from rest_framework.authentication import get_authorization_header
from apps.users.autentication import ExpiringTokenAuthentication
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status

#get_authorization_header se encarga de validar la informacion relacionada al token de la funcion 
class Authentication(object): #autentica el token
    user = None 
    user_token_expired = False
    def get_user(self,request):
        token = get_authorization_header(request).split() #guarda en una variable la informacion validada del token
        if token: #si existe
            try:

                token = token[1].decode() #hace decode o lectura de la pieza 2 del string, osea la data
            except:
                return None
                
                
            token_expire = ExpiringTokenAuthentication() #le agrega expiracion
            user,token,message,self.user_token_expired = token_expire.authenticate_credentials(token) #autentica las credenciales del token que recibe token_expired
            if user != None and token != None: #si existe el token y usuario, los carga y no valdria none
                self.user = user
                return user #asique si existe retorna el usuario
            return message #si no existian
        return None


    def dispatch(self,request,*args,**kwargs): #decide que metodo http usar segun el que le llego por solicitud
        user = self.get_user(request) #recibe las credenciales del user
        if user is not None: #si encontro un token en la peticion y el usuario EXISTIO
            if type(user) == str: #si es string significa que no encontro un usuario y retorno un mensaje
                response= Response({'error': user, 'expired':  self.user_token_expired}, status=status.HTTP_401_UNAUTHORIZED)
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type  = 'application/json'
                response.renderer_context = {}
                return response
            if not self.user_token_expired:
                return super().dispatch(request,*args,**kwargs) #las retorna en el metodo http que le convenga

        response= Response({'error': 'No se han enviado las credenciales.','expired': self.user_token_expired}, status=status.HTTP_400_BAD_REQUEST)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type  = 'application/json'
        response.renderer_context = {}
        return response

##las ultimas 5 lineas funcionan igual que un response con la diferencia 
#de que debemos hacerlo sin libreria Response en el caso de tokens
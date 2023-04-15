from datetime import datetime 
def validate_files(request, field, update = False ): #le enviamos el request y el campo que va a modificar

  #request almacena el request.data 
  
    request._mutable = True

    if update: 
        if type(request[field]) == str:
            del request[field]
#si en el update SI llega una imagen el field no es str y deja la imagen nueva
#si en el update NO llega una imagen, recibe un str y elimina el str que llega
#recordemos que campo vacio se rellena automaticamente con "undefined", por eso 
#el campo genera problemas, xq no espera una cadena de texto
    else:
        request[field] = None if type(request['field']) == str else request ['field']
#el atributo imagen es none si el tipo de dato que le llego es un string. 
#si el tipo de dato no es un string por descarte es un file, entonces almacena la data
    
    request._mutable = False 

    return request

#le da formato legible a la fecha 

def format_date(date):

    date= datetime.strptime(date, '%d/%m/%Y')
    date = f'{date.year} - {date.month} - {date.day}'
    return date

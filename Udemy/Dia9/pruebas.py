import re
# def verificar_email (email):
#     patron = r'[\w\.-]+@[\w\.-]+\.\w+'
#
#     if re.search(patron, email):
#         print ('Email encontrado')
#     else:
#         print('NO encontrado')
#
# verificar_email('@')
# verificar_email('dsds@dssd')
# verificar_email('dsds@dssdsss.com')

# def verificar_saludo(frase):
#     patron = "hola"
#     if re.findall(patron, frase):
#         print("Ok")
#     else:
#         print("No has saludado")
#
#
# verificar_saludo('Hola')

#
# def verificar_cp(cp):
#     patron = r'^[a-zA-Z]{2}\d{4}$'
#     if re.findall(patron, cp):
#         print("Ok")
#     else:
#         print("El código postal ingresado no es correcto")
#
#
# verificar_cp('lf666p')

#
# def verificar_cp(cp):
#     patron = r'^[a-zA-Z]{4}\-\d{5}$'
#     if re.findall(patron, cp):
#         print("Ok")
#     else:
#         print("El código postal ingresado no es correcto")


#verificar_cp('Nter-10596')



def buscador(texto):
    patron = r'[a-zA-Z]{4}\-\d{5}'

    codigo = re.findall(patron, texto)
    if codigo:
        texto = codigo[0]
        texto = texto.replace("'", "")

        return texto
    else:
        return "No se econtro"






print(buscador("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent in tellus porta, vehicula nisl vel, ultrices orci. Mauris egestas, lectus eget consectetur dictum, dui lectus suscipit nulla, vitae tristique elit orci dignissim elit. Sed fermentum elementum Nhjn-54885 odio, sit amet rhoncus nibh pellentesque eu. Proin sit amet porttitor lorem. Cras urna orci, molestie a semper quis, commodo non augue. Vestibulum blandit pellentesque lectus, sit amet dignissim orci finibus quis. In sem metus, pellentesque eget ultrices ac, tempor eleifend ligula."))
print(buscador("Nhjn-54885"))






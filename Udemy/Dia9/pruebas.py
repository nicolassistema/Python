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
    patron = r'^[a-zA-Z]{4}\-\d{5}$'
    codigo = re.findall(patron, texto)
    if codigo:
        return codigo
    else:
        return "No se econtro"






print(buscador("Nter-15046"))






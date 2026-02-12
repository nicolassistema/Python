def decorar_saludo(funcion):
    def otra_funcion(palabra):
        print('hola')
        funcion(palabra)
        print('adios')
    return otra_funcion

@decorar_saludo
def mayusculas(texto):
    print(texto.upper())

def minusculas(texto):
    print(texto.lower())


#mayusculas('hola')

#PAra activar el decorador
minuscula_decorada = decorar_saludo(minusculas)
minuscula_decorada('PALABRA')

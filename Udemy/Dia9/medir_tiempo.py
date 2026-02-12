import time
import timeit


def prueba_for(numero):
    lista = []
    for num in range(1,numero+1):
        lista.append(num)
    return lista


def prueba_while (numero):
    lista = []
    contador = 1
    while contador <= numero:
        lista.append(contador)
        contador += 1
    return lista

# inicio = time.time()
# prueba_for(1000)
# final = time.time()
# print((final - inicio) * 1000, "ms")
#
# inicio = time.time()
# prueba_while(1000)
# final = time.time()
# print((final - inicio) * 1000, "ms")

declaracion = '''
prueba_for(10)
'''
mi_setup = '''
def prueba_for(numero):
    lista = []
    for num in range(1,numero+1):
        lista.append(num)
    return lista

'''

declaracion2 = '''
prueba_while(10)
'''
mi_setup2 = '''
def prueba_while (numero):
    lista = []
    contador = 1
    while contador <= numero:
        lista.append(contador)
        contador += 1
    return lista

'''


duracion = timeit.timeit(declaracion, mi_setup, number= 1000000)
duracion2 = timeit.timeit(declaracion2, mi_setup2, number= 1000000)
print(duracion)
print(duracion2)
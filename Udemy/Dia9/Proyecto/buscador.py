import os
import re
import timeit
import time
import math
import shutil
from datetime import date


def decorador(funcion):
    def otro_decorador():
        hoy = date.today()
        print("----------------------------------------------------")
        print(f"Fecha de busqueda: {hoy}\n")
        print("ARCHIVO\t\tNRO. SERIE")
        print("-------\t\t----------")
        inicio = time.time()
        funcion()
        final = time.time()
        print("Duración de la búsqueda: ", math.floor(final - inicio), "segundos")
        print("----------------------------------------------------")
    return otro_decorador


def buscador(texto):
    patron = r'[a-zA-Z]{4}\-\d{5}'
    # patron = r'^[a-zA-Z]{4}\-\d{5}$'  (^) --> significa que el exto empiece  y $--> que el texto termine asi. En este caso, la expresion regular,
    ## no serviria por que esta indicando que el texto a buscar no tiene que tener nada atras y nada adelante
    codigo = re.findall(patron, texto)
    if codigo:
        texto = codigo[0]
        texto = texto.replace("'", "")

        return texto
    else:
        return ""


ruta = 'C:\\Desarrollo\\Python\\Udemy\\Dia9\\Proyecto\\Mi_Gran_Directorio'
indent = "  "

@decorador
def ejecutar_busqueda():
    contador = 0
    for carpeta, subcarpetas, archivos in os.walk(ruta):
        for archivo in archivos:
            ruta_archivo = os.path.join(carpeta, archivo)
            try:
                with open(ruta_archivo, 'r', encoding='utf-8', errors='ignore') as texto:
                    contenido = texto.read()
                    rasultado =buscador(contenido) if buscador(contenido) != "" else ""

                    if rasultado != "":
                        contador += 1
                        print(f"{archivo}:  {rasultado}")
            except Exception:
                print(f"{indent}    No se pudo leer el archivo")
    print(f"\nNúmeros encontrados: {contador}")

ejecutar_busqueda()





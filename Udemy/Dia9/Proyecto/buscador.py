import os
import re
import timeit
import time
import math
import shutil



def buscador(texto):
    patron = r'^[a-zA-Z]{4}\-\d{5}$'
    codigo = re.findall(patron, texto)
    if codigo:
        return codigo
    else:
        return ""





ruta = 'C:\\Desarrollo\\Python\\Udemy\\Dia9\\Proyecto\\Mi_Gran_Directorio'
indent = "  "
print("----------------------------------------------------")
print(f"ARCHIVO{indent}NRO. SERIE\n-------{indent}----------")


def ejecutar_busqeuda():
    contador = 0
    for carpeta, subcarpetas, archivos in os.walk(ruta):

        nivel = carpeta.replace(ruta, "").count(os.sep)


      # print(f"{indent}{os.path.basename(carpeta)}")
        for archivo in archivos:
         #   print(f"{indent}  {archivo}")
            ruta_archivo = os.path.join(carpeta, archivo)

            try:
                with open(ruta_archivo, 'r', encoding='utf-8', errors='ignore') as texto:
                    contenido = texto.read()
                 #   print(f"{indent}    Tiene {len(contenido)} caracteres")

                    rasultado =buscador(contenido) if buscador(contenido) != "" else ""

                    if rasultado != "":
                        contador += 1
                        print(f"{archivo}:  {rasultado}")



            except Exception:
                print(f"{indent}    No se pudo leer el archivo")
    print(f"\nNúmeros encontrados: {contador}")
inicio = time.time()
ejecutar_busqeuda()
final = time.time()
print("Duración de la búsqueda: " , math.floor(final - inicio) , "segundos")

print("----------------------------------------------------")


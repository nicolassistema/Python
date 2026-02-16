import zipfile
import shutil
import os

'''
COMPRESION Y DESCOMPRESION CON ZIPFILE
'''
#COMPRIMIR
mi_zip = zipfile.ZipFile('sarasa_comprimido_50.zip', 'w')
mi_zip.writestr("archivo_prueba_50.txt", "Este archivo fue creado dentro del zip")


mi_zip.close()
#DESCOMPRIMIR
# zip_abierto = zipfile.ZipFile('sarasa_comprimido.zip', 'r')
# zip_abierto.extractall()

'''
COMPRESION Y DESCOMPRESION CON SHUTIL
'''
#COMPRIMIR
# carpeta_origen = 'C:\\Users\\Usuario\\Desktop\\Python\\Dia9\\Exrtaccion terminadasarasa'
# archivo_destino = 'Todo_Comprimido'
# shutil.make_archive(archivo_destino, 'zip', carpeta_origen)
#
# #DESCOMPRIMIR
# shutil.unpack_archive('sarasa_comprimido.zip','Exrtaccion terminada' 'sarasa')








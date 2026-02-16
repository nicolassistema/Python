import os
import shutil
import send2trash #no es una biblioteca propia de python pero se usa para que cuando se elimine archivos, vayan a la papelera de reciclaje



'''

print(os.getcwd())
archivo = open('archivo_prueba.txt','w')
archivo.write('Texto de prueba')
archivo.close()

print(os.listdir()))#devuelve todos los archivos de una lista

'''

# con shutil podes mover archivos
#shutil.move('archivo_prueba.txt','C:\\Users\\Usuario\\Desktop\\archivo_prueba.txt')
#shutil.move('C:\\Users\\Usuario\\Desktop\\archivo_prueba.txt','archivo_prueba.txt')


#para eliminar archivos y mandarlos a la papelera
#send2trash.send2trash('archivo_prueba.txt')



ruta = 'C:\\Desarrollo\\Python\\Udemy'
#recorre todo el contenido de la carpeta
# for carpeta, subcarpeta, archivo in os.walk(ruta):
#
#     print(f'en la carpeta{carpeta}')
#     print(f' las sub carpetas son:')
#     for sub in subcarpeta:
#         print(f'\t{sub}')
#         print('     los archivos son:')
#         for arch in archivo:
#             if arch.startswith('Pruebas'):# sirve para buscar un archivo en particular
#                 print(f'\t{arch}')
#         print('\n')


for carpeta, subcarpetas, archivos in os.walk(ruta):
    nivel = carpeta.replace(ruta, "").count(os.sep)
    indent = "  " * nivel

    print(f"{indent}{os.path.basename(carpeta)}")

    for archivo in archivos:
        print(f"{indent}  {archivo}")


#print(os.walk('C:\\Users\\Usuario\\Desktop\\'))


#print(os.listdir())



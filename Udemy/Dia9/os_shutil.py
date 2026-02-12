import os
import shutil
import send2trash #no es una biblioteca propia de python pero se usa para que cuando se elimine archivos, vayan a la papelera de reciclaje



'''

print(os.getcwd())
archivo = open('archivo_prueba.txt','w')
archivo.write('Archivo de prueba')
archivo.close()

'''

# con shutil podes mover archivos
#shutil.move('archivo_prueba.txt','C:\\Users\\Usuario\\Desktop\\archivo_prueba.txt')
#shutil.move('C:\\Users\\Usuario\\Desktop\\archivo_prueba.txt','archivo_prueba.txt')

#send2trash.send2trash('archivo_prueba.txt')

ruta = 'C:\\Users\\Usuario\\Desktop\\Python\\Dia8'

for carpeta, subcarpeta, archivo in os.walk(ruta):

    print(f'en la carpeta{carpeta}')
    print(f' las sub carpetas son:')
    for sub in subcarpeta:
        print(f'\t{sub}')
        print('los archivos son:')
        for arch in archivo:
            if arch.startswith('Ejercicio'):# sirve para buscar un archivo en particular
                print(f'\t{arch}')
        print('\n')





#print(os.walk('C:\\Users\\Usuario\\Desktop\\'))


#print(os.listdir())



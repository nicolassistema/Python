mi_archivo = open("archivo.txt",'w')

#print(mi_archivo.read())

#una_linea = mi_archivo.readlines()
#print(una_linea)


mi_archivo.write('contenido nuevo')
mi_archivo.close()

mi_archivo = open("archivo.txt",'r')


print(mi_archivo.read())















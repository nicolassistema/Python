import cv2
from cv2 import *
import face_recognition as fr
import os
import numpy as np
from datetime import datetime


#crear una base de datos
ruta = 'Empleados'
mis_imagenes =  []
nombres_empleados = []
lista_empleados = os.listdir(ruta)

for nombre in lista_empleados:
    imagen_actual = cv2.imread(f'{ruta}/{nombre}')
    mis_imagenes.append(imagen_actual)
    nombres_empleados.append(os.path.splitext(nombre)[0])


print(nombres_empleados)

#codificar imagenes
def codificar(imagenes):
    #crear una lista nueva
    lista_codificada = []

    #pasar todas las imagenes a rgb
    for imagen in imagenes:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGRA2BGR)

        #codificar
        codificado = fr.face_encodings(imagen)[0]

        #agregar a lista
        lista_codificada.append(codificado)

    return lista_codificada


#registrar los ingresos
def registrar_ingresos(persona):
 f = open('registro.csv','r+')
 lista_datos = f.readlines()
 nombre_registro = []
 for linea in lista_datos:
     ingresos = linea.split(',')
     nombre_registro.append(ingresos[0])

     if persona not in nombre_registro:
         ahora = datetime.now()
         string_ahora = ahora.strftime("%H:%M:%S")
         f.write(f'\n{persona},{string_ahora}')


lista_empleados_codificada = codificar(mis_imagenes)

#tomar una imagen de camara web
captura = cv2.VideoCapture(0,cv2.CAP_DSHOW)

#leer imagen de la camara
exito, imagen = captura.read()

if not exito:
    print('No hay imagen')
else:
    #reconocer camara en captura
    cara_captura = fr.face_locations(imagen)

    #codifcar cara para captura
    cara_captura_codificada = fr.face_encodings(imagen,cara_captura)

    #buscar coincidencias
    for caracodif, caraubic in zip(cara_captura_codificada,cara_captura):
        coincidencias = fr.compare_faces(lista_empleados_codificada,caracodif)
        distancias = fr.face_distance(lista_empleados_codificada,caracodif)

        print(distancias)

        indice_coincidencia = np.argmin(distancias)

        #mostrar coincidencia si las hay
        if distancias[indice_coincidencia] > 0.6:
            print('No coincide con ninguno de nuestros empleados')
        else:

            print('Bienvenido empleado')
            #buscar el nombre del empleado encontrado
            nombre = nombres_empleados[indice_coincidencia]

            y1, x2, y2, x1 = caraubic
            cv2.rectangle(imagen,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(imagen,(x1,y2 - 35),(x2,y2),(0,0,255),cv2.FILLED)
            cv2.putText(imagen, nombre, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,2555,255), 2)


            registrar_ingresos(nombre)


            #motrar la imagen obtenida
            cv2.imshow('Imagen web', imagen)

            #mantener ventana abiera
            cv2.waitKey(0)






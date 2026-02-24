import bs4 #permite navegar en el texto html y buscar lo que necesitamos
import requests


resultado = requests.get('https://www.escueladirecta.com/p/excel-aplicado-al-analisis-financiero')

sopa = bs4.BeautifulSoup(resultado.text, 'lxml')

# imagenes = sopa.select('img')
#
#
# for imagen in imagenes:
#     print(imagen.get('src'))
#

imagenes = sopa.select('img')[2]['src']
print(imagenes)



imagen_curso_1 = requests.get(imagenes)
print(imagen_curso_1.content)

#genero un archivo y guardo la imagen en el
f = open('mi_imagen.jpg', 'wb')
f.write(imagen_curso_1.content)
f.close()
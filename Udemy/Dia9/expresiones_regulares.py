import re


texto = 'Los párrafos cortos son aquellos párrafos que tienen entre tres y seis líneas. 666-569-6999 Si bien existen párrafos más extensos, que pueden llegar hasta las veinte líneas, lo recomendable es que un párrafo no tenga más de cuatro o cinco oraciones. Un párrafo es una unidad de un texto compuesta por una o varias oraciones, que comienza con una mayúscula y que termina con un punto y aparte. Los textos se organizan de manera tal que cada párrafo trata sobre una idea central. Generalmente, la primera oración de cada párrafo suele explicitar cuál es el punto principal que se desarrollará.'


patron = 'papa'
busqueda = re.findall(patron, texto)


patron2 = r'\d\d\d-\d\d\d-\d\d\d\d'
resultado2 = re.findall(patron2, texto)

print(resultado2)

clave = input("Clave: ")
patron3 = r'\D{1}\w{7}' #expresion regular
chequear = re.search(patron3, clave)

print(chequear)






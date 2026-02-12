texto = "Esta es una prueba"
indice = texto[-4]
print(indice)


subString = texto[0:4:2]



resultado = texto.index("e",9)
print(subString)

lista1= [1,2,3]
lista2= [4,5,6]
lista3= [7,8,9]

diccionario = {"obj1":lista1,"obj2":"Hola","obj2":lista3}

print(diccionario)

numerUno = 2
numerDos = 2


if numerUno<numerDos:
    print("el primer numero es menor que el segundo")
elif numerUno>numerDos:
    print("El segundo numero es mayor que el primero")
else:
    print("Los numeros son iguales")


listaNobres = ['Nicolas','Ezequiel','Loly']

for elemento in listaNobres:
    if elemento=="Nicolas":
        print("Hola "  + elemento)
    else:
        print("No existe op")





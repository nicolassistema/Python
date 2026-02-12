'''
try:
    # Codigo que queremos prbar
    print("hi")
except:
    # codigo a ejecutar si  hay error
    print("nacer")
else:
    # Codigo a ejecutar si no hay un error
    print("nacer")
finally:
    # Codigo que se va a ejecutar de todos modos
    print("nacer")


# Errores personalizados
try:
    # Codigo que queremos prbar
    print("hi")
except TypeError:
    # codigo a ejecutar si  hay error
    print("Estas intentando concatenar distintos tipos")
except ValueError:
    # codigo a ejecutar si  hay error
    print("Ese no es un numero")
else:
    # Codigo a ejecutar si no hay un error
    print("Hiciste todo bien")
finally:
    # Codigo que se va a ejecutar de todos modos
    print("Eso fue todo")
'''

# ejemplo ingreso incorrecto
def pedir_numero():
    while True:
        try:
            numero = int(input("Ingrese un numero: "))
        except:
            print("Ese no es un numero")
        else:
            print(f"Ingresaste el numero {numero}")
            break
pedir_numero()
print("Gracias por usar")


numero = 23

print(Numero)





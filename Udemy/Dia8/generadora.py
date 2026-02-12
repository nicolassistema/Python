# van guardando lo que se le pide, mas que nada para no ocupar memoria, solo a demanda
# Se puede usar como un incrementador de id a medida que se genera un objeto
def mi_generador():
    for x in range(1,10):
        yield x


g = mi_generador()
print(next(g))
print(next(g))
print(next(g))

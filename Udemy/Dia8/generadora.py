# van guardando lo que se le pide, mas que nada para no ocupar memoria, solo a demanda
# Se puede usar como un incrementador de id a medida que se genera un objeto
# def mi_generador():
#     for x in range(1,10):
#         yield x
#
#
# g = mi_generador()
# print(next(g))
# print(next(g))
# print(next(g))


def descontar_vidas():
    num = 4
    while True:
        num -= 1
        if num != 0:
            mensaje = f"Te {'queda' if num == 1 else 'quedan'} {num} vida{'s' if num != 1 else ''}"

        else:
            mensaje = "Game Over"

        yield mensaje


perder_vida = descontar_vidas()

print(next(perder_vida))
print(next(perder_vida))
print(next(perder_vida))
print(next(perder_vida))
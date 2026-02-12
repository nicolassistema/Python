def funcion(entrada):
    print(entrada)


funcion("Hola ")



def contar_primos(numero_a, numero_b):
    cero = 0

    for i in range(numero_a,numero_b):
        if i != 0:
            if i != 1:
                if i % 2 != 0:
                    cero += 1
                    #print(i)
    print(cero)

contar_primos(-99999999,99999999)









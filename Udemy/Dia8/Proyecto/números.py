def decorar_turno(funcion):
    def otra_funcion(sector):
        print('Su turno es')
        resultado = funcion(sector)
        print('Aguarde y sera atendido')
        return resultado
    return otra_funcion


def generador_turno():
    n = 1
    while True:
        yield n
        n += 1


def inicializar_sectores():
    c = generador_turno()
    f = generador_turno()
    p = generador_turno()
    lista_sector = [c, f, p]
    return lista_sector

lista_sectores = inicializar_sectores()


@decorar_turno
def switch_sectores(sector):
    if sector == 1: #sector c --> 1
         print('C-' + str(next(lista_sectores[0])))
    elif sector == 2: #sector f --> 2
        print('F-' + str(next(lista_sectores[1])))
    else: #sector p--> 3
        print('P-' + str(next(lista_sectores[2])))





#
# switch_sectores(1)
# switch_sectores(1)
# switch_sectores(2)
# switch_sectores(1)

turno_decorado = decorar_turno(switch_sectores)
turno_decorado(1)

class Pajaro:
    # es el atributo de la clase ya en el constructor

    algo = "verde"  # variable de clase

    def __init__(self,color, tamanio):# atributo de instancia
        self.color = color
        self.tamanio = tamanio
    #metodos de instancias
    def piar(self):#metodo que usar la instancia
        print('pio, mi color {}'.format(self.color))

    def volar(metros):
        print(f"El pajaro volo {metros} metros")

    #metodos de clase
    @classmethod
    def poner_huevos(cls,cantidad):
        print(f"la cantidad de hievos es {cantidad}")

    #metodos estaticos
    @staticmethod
    def mirar():
        print("mi color")


mi_pajaro = Pajaro("rojo",12)

mi_pajaro.mirar()






#mi_pajaro.tamanio = 23
#mi_pajaro.piar()







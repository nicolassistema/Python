from Animal import Animal
from Herencia import Pajaro


class Hija(Animal,Pajaro):
    def __init__(self,cantidad,tamanio):
        self.cantidad = cantidad
        self.tamanio = tamanio

hija1 = Hija(12,56)

hija1.nacer()






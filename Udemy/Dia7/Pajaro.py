from Animal import Animal


class Pajaro(Animal):

    def __init__(self,  edad, color, altura_vuelo):
        super().__init__(edad, color)
        self.altura_vuelo = altura_vuelo






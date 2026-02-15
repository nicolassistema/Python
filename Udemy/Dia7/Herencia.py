class Padre:
    def hablar(self):
        print("Hola")



class Madre:
    def reir(self):
        print("jaja")


class Hijo(Padre, Madre):
    pass




class Nieto(Hijo):
    pass


mi_nieto = Nieto()

mi_nieto.reir()
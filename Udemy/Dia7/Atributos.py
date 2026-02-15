class PajaroUno:

    #propiedad que corresponde a la clase, no a la instancia
    alas = True


    #__init__ es un metodo especial pero se puede comportar como un Construcotr de la clase en este caso
    #self --> es obligatorio
    def __init__(self, color, especie = None):#el segundo parametro (especie = None) es un parametro opcional, como para simular sobre carga en el cosntructor
        #Atributos
        self.color = color
        self.especie = especie

    #metodos de instancia por que tienen el 'self'
    def piar(self):
        print('pio, mi color es {}'.format(self.color))

    def volar(self, metros):
        print(f"el pajaro a volado una cantidad de {metros} metros")

    #metodos de clas
    @classmethod #--> es un decorador
    def poner_huevos(cls, cantidad):
        print(f"Poner {cantidad} huevos")


    #los metodos estaticos no pueden acceder ni a los atrubutos de la clase, ni de la instancia
    @staticmethod
    def mirar():
        print('El pajaro mira')


#mi_pajaro = Pajaro('Verde')


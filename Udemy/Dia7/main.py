import Atributos
from Pajaro import  Pajaro

#
# mi_pajaro = Atributos.PajaroUno('Verde', 'carpintero')
#
#
#
# print(mi_pajaro.color)
# print(mi_pajaro.especie)
#
#
# mi_pajaro.volar(10)
# print(mi_pajaro.volar)
#
#
# mi_pajaro.poner_huevos(10)
# print(mi_pajaro)
#
#
# mi_pajaro.mirar()

piolin = Pajaro(edad=2, color="amarillo")
piolin.nacer()
print(piolin.edad, piolin.color)

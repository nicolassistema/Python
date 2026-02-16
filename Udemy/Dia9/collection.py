from collections import Counter
from collections import defaultdict
# tupla nominada
from collections import namedtuple


frase = 'al pan pan y al vino vino'
# el counter cuanta palabras, caracteres, etc y devuelve como un diccion ario con el objeto y la cantidad
print(Counter(frase.split()))


# devuelve la lista con la cantidad por objeto de manera ordenada por mas aparciones
serie = Counter([1,1,1,1,1,2,2,2,2,3,3,3,3,3,3,4])
print(serie.most_common())

#devueve el valor de la clave, en este caso 'rojo'
mi_dic= {'uno': 'rojo', 'dos': 'verde', 'tres': 'azul'}
print(mi_dic['uno'])



#cuando se quiere traer un elemento del diccionario, le podemos poner que si no existe, que devuelva algo
mi_dic_dos = defaultdict(lambda : '####nada' )
mi_dic_dos['uno'] = 'rojo'
print(mi_dic_dos['unj'])


#Tupla nominada --> es como que creo un objeto, lo instancio y accedemos a los atributos
Persona = namedtuple('Persona', ['nombre', 'apellido','edad'])

nicolas = Persona('nicola', 'letticugna', 18)

setattr(nicolas, 'nicola', 'gomes')
print(nicolas.apellido)
print(nicolas.nombre)













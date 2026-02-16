
import  datetime
from datetime import datetime


#funciona con la biblioteca  import  datetime
# mi_hora = datetime.time(17, 12)
# print(mi_hora.minute)
# print(mi_hora.hour)
# print(mi_hora.microsecond)


#funciona con la biblioteca  import  datetime
#mi_dia = datetime.date(2025, 12, 31, 10, 15, 2500)

#solo la fecha de hoy
#print(mi_dia.today())


mi_fecha = datetime(2025, 5, 31, 10, 15, 0,1500)


mi_fecha = mi_fecha.replace(month=10)

print(mi_fecha)

mi_dia_dos = datetime(2025, 12, 31, 10, 15, 0)




# #devuelve la fecha, hora, miuntos, segundos y milesima de ahora y funciona con
# ahora = datetime.datetime.now()
# print(ahora.strftime("%H:%M:%S.%f")[:-3])

from datetime import datetime
despertar = datetime(2025,11,11, 5, 0 )
dormir = datetime (2025,12,31, 23, 0 )
vida = dormir - despertar
print(vida.seconds)


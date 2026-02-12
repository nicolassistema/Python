import  datetime

mi_hora = datetime.time(17, 12)





mi_dia = datetime.date(2025, 12, 31)
print(mi_hora.minute)
print(mi_hora.hour)
print(mi_hora.microsecond)

print(mi_dia.today())

from datetime import datetime
despertar = datetime(2025,11,11, 5, 0 )
dormir = datetime (2025,12,31, 23, 0 )
vida = dormir - despertar
print(vida.seconds)


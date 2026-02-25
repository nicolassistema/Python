from tkinter import *


#iniciar tkinter
aplicacion = Tk()

#tamaño de la ventana
aplicacion.geometry('1020x630+0+0')

#evitar maximizar
aplicacion.resizable(0, 0)

#titulo de la ventana
aplicacion.title('mi restaurante - sistema de facturacion')

#color de fondo de la ventana
aplicacion.configure(bg='burlywood')

#panel superior
panel_superior = Frame(aplicacion,bd=1, relief = FLAT)
panel_superior.pack(side=TOP)

#etiqueta titulo
teiqueta_titulo = Label(panel_superior, text = 'Sistema de facturacion',  fg = 'azure4',
                        font=('Dosis', 58), bg='burlywood', width = 27)
teiqueta_titulo.grid(row=0,column=0)

#panel izquierdo
panel_izquierdo = Frame(aplicacion, bd = 1, relief = FLAT)
panel_izquierdo.pack(side=LEFT)

#Panel comidas
panel_comidas = LabelFrame(panel_izquierdo, text = 'Comidas', font=('Dosis',19,'bold'),bd=1,relief=FLAT , fg = 'azure4',)
panel_comidas.pack(side=LEFT)

#Panel bebidas
panel_bebidas = LabelFrame(panel_izquierdo, text = 'Bebidas', font=('Dosis',19,'bold'),bd=1,relief=FLAT , fg = 'azure4',)
panel_bebidas.pack(side=LEFT)

#Panel postres
panel_postres = LabelFrame(panel_izquierdo, text = 'Bebidas', font=('Dosis',19,'bold'),bd=1,relief=FLAT , fg = 'azure4',)
panel_postres.pack(side=LEFT)

#panel derecha
panel_derecha = Frame(aplicacion, bd=1, relief = FLAT)
panel_derecha.pack(side=RIGHT)

#panel calculadora
panel_calculadora = Frame(panel_derecha, bd = 1 , relief = FLAT, bg = 'burlywood')
panel_calculadora.pack(side=RIGHT)

#panel botones
panel_botones = Frame(panel_derecha, bd = 1 , relief = FLAT, bg = 'burlywood')
panel_botones.pack(side=RIGHT)

#panel costos
panel_costos = Frame(panel_izquierdo, bg = 'black', relief = FLAT)
panel_costos.pack(side=BOTTOM)

#listas de productos
lista_comidas = ['pollo','cordero','salmon','merluza','kebab', 'pizza1', 'pizza2', 'pizza3']
lista_bebidas = ['egua','soda','jugo','cola','vino1', 'vino2', 'cerveza1', 'cerveza2']
lista_postres = ['helado','futa','brownies','flan','mouse','pastel1','pastel2','pastel3']


#generer items bebida
variables_bebida =[]

contador = 0

for bebida in lista_bebidas:
    variables_bebida.append('')
    variables_bebida[contador] = IntVar()
    comida = Checkbutton(panel_bebidas,text=bebida.title(), font=('Dosis',19,'bold'),
                         onvalue=1, offvalue=0,variable=variables_bebida[contador])
    comida.grid(row=contador,column=0, sticky=W)
    contador += 1



#generer items postres
variables_postres =[]

contador = 0

for postres in lista_postres:
    variables_postres.append('')
    variables_postres[contador] = IntVar()
    postres = Checkbutton(panel_postres,text=postres.title(), font=('Dosis',19,'bold'),
                         onvalue=1, offvalue=0,variable=variables_postres[contador])
    postres.grid(row=contador,column=0, sticky=W)
    contador += 1


#generer items comida
variables_comida =[]

contador = 0

for comida in lista_comidas:
    variables_comida.append('')
    variables_comida[contador] = IntVar()
    comida = Checkbutton(panel_comidas,text=comida.title(), font=('Dosis',19,'bold'),
                         onvalue=1, offvalue=0,variable=variables_comida[contador])
    comida.grid(row=contador,column=0, sticky=W)
    contador += 1





#evitar que la pantalla se cierre
aplicacion.mainloop()



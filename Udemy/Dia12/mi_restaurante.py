from tkinter import *


#iniciar tkinter
aplicacion = Tk()

#tamaño de la ventana
aplicacion.geometry('1020x630+0+0')

#evitar maximizar
aplicacion.resizable(0, 0)

#titulo de la ventana
aplicacion.title('Mi restaurante - sistema de facturacion')

#color de fondo de la ventana
aplicacion.configure(bg='burlywood')

#panel superior
panel_superior = Frame(aplicacion,bd=1, relief = FLAT)
panel_superior.pack(side=TOP)

#etiqueta titulo
teiqueta_titulo = Label(panel_superior,
                        text = 'Sistema de facturacion',
                        fg = 'azure4',
                        font=('Dosis', 58),
                        bg='burlywood',
                        width = 27)
teiqueta_titulo.grid(row=0,
                     column=0)

#panel izquierdo
panel_izquierdo = Frame(aplicacion, bd = 1, relief = FLAT)
panel_izquierdo.pack(side=LEFT)

#panel costos
panel_costos = Frame(panel_izquierdo, bd = 1, relief = FLAT, bg='azure4', padx=40)
panel_costos.pack(side=LEFT)
panel_costos.pack(side=BOTTOM)

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



#listas de productos
lista_comidas = ['pollo','cordero','salmon','merluza','kebab', 'pizza1', 'pizza2', 'pizza3']
lista_bebidas = ['egua','soda','jugo','cola','vino1', 'vino2', 'cerveza1', 'cerveza2']
lista_postres = ['helado','futa','brownies','flan','mouse','pastel1','pastel2','pastel3']



#generer items comida
variables_comida =[]
texto_comida = []
cuadros_comida = []
contador = 0

for comida in lista_comidas:

    # crear checkbuttom
    variables_comida.append('')
    variables_comida[contador] = IntVar()
    comida = Checkbutton(panel_comidas,
                         text=comida.title(),
                         font=('Dosis', 19, 'bold'),
                         onvalue=1,
                         offvalue=0,
                         variable=variables_comida[contador])
    comida.grid(row=contador,
                column=0,
                sticky=W)

    # crear los cuadros de entrada
    cuadros_comida.append('')
    texto_comida.append('')
    texto_comida[contador] = StringVar()
    texto_comida[contador].set('0')
    cuadros_comida[contador] = Entry(panel_comidas,
                                     font=('Dosis', 18, 'bold'),
                                     bd=1,
                                     width=6,
                                     state=DISABLED,
                                     textvariable=texto_comida[contador])
    cuadros_comida[contador].grid(row=contador,
                                  column=1,)
    contador += 1


# generer items bebida
variables_bebida = []
texto_bebida = []
cuadros_bebida = []
contador = 0

for bebida in lista_bebidas:
    # crear check buttom
    variables_bebida.append('')
    variables_bebida[contador] = IntVar()
    bebida = Checkbutton(panel_bebidas,
                         text=bebida.title(),
                         font=('Dosis', 19, 'bold'),
                         onvalue=1,
                         offvalue=0,
                         variable=variables_bebida[contador])
    bebida.grid(row=contador,
                column=0,
                sticky=W)

    # crear los cuadros de entrada
    cuadros_bebida.append('')
    texto_bebida.append('')
    texto_bebida[contador] = StringVar()
    texto_bebida[contador].set('0')
    cuadros_bebida[contador] = Entry(panel_bebidas,
                                     font=('Dosis', 18, 'bold'),
                                     bd=1,
                                     width=6,
                                     state=DISABLED,
                                     textvariable=texto_bebida[contador])
    cuadros_bebida[contador].grid(row=contador,
                                  column=1,)

    contador += 1


#generer items postres
variables_postres =[]
texto_postres = []
cuadros_postres = []
contador = 0

for postres in lista_postres:
    variables_postres.append('')
    variables_postres[contador] = IntVar()
    postres = Checkbutton(panel_postres,
                          text=postres.title(),
                          font=('Dosis',19,'bold'),
                          onvalue=1,
                          offvalue=0,
                          variable=variables_postres[contador])
    postres.grid(row=contador,
                 column=0,
                 sticky=W)

    # crear los cuadros de entrada
    cuadros_postres.append('')
    texto_postres.append('')
    texto_postres[contador] = StringVar()
    texto_postres[contador].set('0')
    cuadros_postres[contador] = Entry(panel_postres,
                                     font=('Dosis', 18, 'bold'),
                                     bd=1,
                                     width=6,
                                     state=DISABLED,
                                     textvariable=texto_postres[contador])
    cuadros_postres[contador].grid(row=contador,
                                  column=1,)


    contador += 1





#variables
var_costo_comida = StringVar()
var_costo_bebida = StringVar()
var_costo_postre = StringVar()
var_subtotal = StringVar()
var_impuestos = StringVar()
var_total = StringVar()

#etiquetas de costos y campos de entrada
etiqueta_costo_comida = Label(panel_costos,
                              text="Costo Comida",
                              font = ('Dosis', 12, 'bold'),
                              bg='azure4',
                              fg='white',)

etiqueta_costo_comida.grid(row=0,
                           column=0)

texto_costo_comida = Entry(panel_costos,
                           font=('Dosis', 18, 'bold'),
                           bd=1,
                           width=10,
                           state='readonly',
                           textvariable=var_costo_comida)
texto_costo_comida.grid(row=0,
                        column=1, padx=41)




#etiquetas de costos y campos de entrada
etiqueta_costo_bebida = Label(panel_costos,
                              text="Costo bebida",
                              font = ('Dosis', 12, 'bold'),
                              bg='azure4',
                              fg='white',)

etiqueta_costo_bebida.grid(row=1,
                           column=0)

texto_costo_bebida = Entry(panel_costos,
                           font=('Dosis', 18, 'bold'),
                           bd=1,
                           width=10,
                           state='readonly',
                           textvariable=var_costo_bebida)
texto_costo_bebida.grid(row=1,
                        column=1, padx=41)



#etiquetas de costos y campos de entrada
etiqueta_costo_postre = Label(panel_costos,
                              text="Costo postre",
                              font = ('Dosis', 12, 'bold'),
                              bg='azure4',
                              fg='white',)

etiqueta_costo_postre.grid(row=2,
                           column=0)

texto_costo_postre = Entry(panel_costos,
                           font=('Dosis', 18, 'bold'),
                           bd=1,
                           width=10,
                           state='readonly',
                           textvariable=var_costo_postre)
texto_costo_postre.grid(row=2,
                        column=1, padx=41)


#etiquetas de costos y campos de entrada
etiqueta_subtotal = Label(panel_costos,
                              text="subtotal",
                              font = ('Dosis', 12, 'bold'),
                              bg='azure4',
                              fg='white',)

etiqueta_subtotal.grid(row=0,
                        column=2)

texto_subtotal = Entry(panel_costos,
                           font=('Dosis', 18, 'bold'),
                           bd=1,
                           width=10,
                           state='readonly',
                           textvariable=var_subtotal)
texto_subtotal.grid(row=0,
                        column=3, padx=41)


#etiquetas de costos y campos de entrada
etiqueta_impuestos = Label(panel_costos,
                              text="impuestos",
                              font = ('Dosis', 12, 'bold'),
                              bg='azure4',
                              fg='white',)

etiqueta_impuestos.grid(row=1,
                        column=2)

texto_impuestos = Entry(panel_costos,
                           font=('Dosis', 18, 'bold'),
                           bd=1,
                           width=10,
                           state='readonly',
                           textvariable=var_impuestos)
texto_impuestos.grid(row=1,
                        column=3, padx=41)


#etiquetas de costos y campos de entrada
etiqueta_total = Label(panel_costos,
                              text="total",
                              font = ('Dosis', 12, 'bold'),
                              bg='azure4',
                              fg='white',)

etiqueta_total.grid(row=2,
                        column=2)

texto_total = Entry(panel_costos,
                           font=('Dosis', 18, 'bold'),
                           bd=1,
                           width=10,
                           state='readonly',
                           textvariable=var_total)
texto_total.grid(row=2,
                        column=3, padx=41)



#evitar que la pantalla se cierre
aplicacion.mainloop()



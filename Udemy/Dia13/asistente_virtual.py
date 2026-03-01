import re
import unicodedata
import datetime
import pyttsx3
import speech_recognition as sr
import pywhatkit

import yfinance as yf
import pyjokes
import webbrowser
import wikipedia
import pyaudio
from edge_tts import voices



def normalizar_texto(txt: str) -> str:
    if not txt:
        return ""

    txt = txt.strip().lower()

    # Quitar tildes/acentos (qué -> que, día -> dia)
    txt = unicodedata.normalize("NFD", txt)
    txt = "".join(ch for ch in txt if unicodedata.category(ch) != "Mn")

    # Sacar puntuación y dejar letras/números/espacios
    txt = re.sub(r"[^a-z0-9\s]", " ", txt)

    # Espacios múltiples a uno solo
    txt = re.sub(r"\s+", " ", txt).strip()

    return txt




#opciones de voz/idioma
id1= r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'
id2= r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
id3= r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'



#escuchar nuestro microno y devolver el audio como texto

def transformar_audio_en_texto():
    r = sr.Recognizer()

    #configurar el microfono
    with sr.Microphone() as origen:

        #tiempo de espera
        r.pause_threshold = 0.8

        #informar que comenzo la grabacion
        print("ya puede hablar")

        #guardar lo que escuche como audio
        audio = r.listen(origen)

        try:
            #buscar en google
            pedido = r.recognize_google(audio, language='es-ar')

            #prueba de que pueodo ingresar
            print("Dijiste:" + pedido)

            #devolver pedido
            return  pedido

        #en caso de que no comprenda el audio
        except sr.UnknownValueError:

            #prueba de que no comprendio el audio
            print("ups, no entendi")


            #devolver error
            return "Sigo esperando"

        #en caso de no resolver el pedido
        except sr.RequestError:
            # prueba de que no comprendio el audio
            print("ups, no hay servicio")

            # devolver error
            return "Sigo esperando"


        #error inesperado
        except :
            # prueba de que no comprendio el audio
            print("ups, algo a salido mal")

            # devolver error
            return "Sigo esperando"

#transformar_audio_en_texto()



#funciona para que el asistente pueda ser escuchado

def hablar(mensaje):

    #encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id3)

    #pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()

# engine = pyttsx3.init()
# for voz in engine.getProperty('voices'):
#     print(voz)

#informar el idia de la semana
def pedir_dia():

    #crear variable con datos de hoy
    dia = datetime.date.today()
    #print(dia)

    #crear variable para el dia de la semana
    dia_demana = dia.weekday()
    #print(dia_demana)

    #diccionario
    calendario ={0: 'lunes',
                 1: 'martes',
                 2: 'miercoles',
                 3: 'jueves',
                 4: 'viernes',
                 5: 'sabado',
                 6: 'domingo'
                 }

    #decir el dia de la semana
    hablar(f'Hoy es {calendario[dia_demana]}')
#hablar("hola mundo")


#Informar que hora eso
def pedir_hora():
    #crear variable con datos de la hora
    hora=datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} horas con {hora.minute} minutos'

    print(hora)

    #decir la hora
    hablar(hora)

# pedir_dia()
# pedir_hora()

#funcion saludo inicial
def saludo_inicial():

    #Crear variable con datos de hora
    hora = datetime.datetime.now()

    if hora.hour < 6 or hora.hour > 20:
        momneto = 'buenas noches'
    elif hora.hour >= 6 and hora.hour < 13:
        momento = 'Buenos Dias'
    else:
        momento = 'Buenas tardes'

    #decir el slaudo
    hablar(f'{momento} soy computadora de la nave, tu asistente personal. Por favor, dime en que te puedo ayudar')

#saludo_inicial()

#funcion central del asistente
def pedir_cosas():

    saludo_inicial()
    comenzar = True

    while comenzar:

        pedido_raw = transformar_audio_en_texto()

        # si no entendió, que siga escuchando
        if not pedido_raw or pedido_raw == "Sigo esperando":
            continue

        pedido = normalizar_texto(pedido_raw)

        if 'abrir youtube' in pedido:
            hablar('con gusto, estoy abriendo youtube')
            webbrowser.open('https://www.youtube.com/')
            continue

        elif 'abrir navegador' in pedido:
            hablar('Claro, estoy en eso')
            webbrowser.open('https://www.google.com/')
            continue

        elif 'que dia es' in pedido:
            pedir_dia()
            continue

        elif 'que hora es' in pedido:
            pedir_hora()
            continue

        # wikipedia: flexible
        elif 'wikipedia' in pedido and ('busca' in pedido or 'buscar' in pedido):
            hablar('Buscando en wikipedia')
            consulta = pedido.replace('busca en wikipedia', '')
            consulta = consulta.replace('buscar en wikipedia', '')
            consulta = consulta.strip()

            wikipedia.set_lang('es')
            resultado = wikipedia.summary(consulta, sentences=1)

            hablar('Wikipedia dice lo siguiente:')
            hablar(resultado)
            continue

        elif 'buscar en internet' in pedido:#Esto busca por cualquier cosa en goolge
            hablar('Ya mismo estoy en eso')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            continue

        elif 'reproducir' in pedido:
            hablar('buscando reproduccion')
            pywhatkit.playonyt(pedido)
            continue
        elif 'broma' in pedido:
            hablar(pyjokes.get_joke(language='es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple':'APPL',
                       'amazon':'AMZN',
                       'google':'GOOGL'
                       }

            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontre, el precio actual de {accion} es {precio_actual}')
                continue
            except :
                hablar('Perdon pero no la he encontrado')
                continue

        else:
            comenzar = False


pedir_cosas()


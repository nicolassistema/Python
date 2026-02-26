import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance
import pyjokes
import webbrowser
import wikipedia
import pyaudio

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
            respuesta = pedido

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

transformar_audio_en_texto()




# Bibliotecas que estão sendo utilizadas
import speech_recognition as sr
import pyttsx3
import wikipedia
import pywhatkit
import openai
import pyaudio
import PyInstaller
from datetime import datetime
import requests


# Conectar minha chave API
api_key = "474bf4dc0d66c32d1484c9a9da9581f7"

# Função para saber o horário


def horas_atual():
    now = datetime.now()
    return now.strftime('Hoje é %d de %B e são %H:%M horas.')

# Função para obter a temperatura em São Paulo


def get_temperature_sao_paulo():
    url = f'http://api.openweathermap.org/data/2.5/weather?q=Sao Paulo,br&appid={
        api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    temperature = data['main']['temp']
    return temperature


audio = sr.Recognizer()
maquina = pyttsx3.init()
# Função para da máquina escuta


def listen_command():
    comando = None  # Adicione esta linha para atribuir um valor inicial a 'comando'
    try:
        with sr.Microphone() as source:
            print('Ouvindo...')
            voz = audio.listen(source)
            comando = audio.recognize_google(voz, language='pt-BR')
            comando = comando.lower()

            if 'Ivi' in comando:
                comando = comando.replace('Ivi', '')
                maquina.say(comando)
                maquina.runAndWait()

    except Exception as e:
        print(f'Não estou detectando o microfone: {e}')

    return comando


def execute_command():

    comando = listen_command()

    if comando is not None:

        if 'que horas são' in comando:
            maquina.say(horas_atual())
            maquina.runAndWait()
        else:  # Adicione esta linha para verificar se 'comando' foi atribuído um valor antes de ser usado

            if 'procure por' in comando:
                procurar = comando.replace('procure por', '')
                wikipedia.set_lang('pt')
                resultado = wikipedia.summary(procurar, 2)
                print(resultado)
                maquina.say(resultado)
                maquina.runAndWait()

            elif 'toque' in comando:
                musica = comando.replace('toque', '')
                resultado = pywhatkit.playonyt(musica)
                maquina.say(f'Tocando {musica} no youtube')
                maquina.runAndWait()

            elif 'pare' in comando:
                print("Fala Parada")
                maquina.stop()
                maquina.runAndWait()

            elif 'quantos graus' in comando:
                temperatura = get_temperature_sao_paulo()
                print(f'A temperatura em São Paulo é de {
                      temperatura} graus Celsius.')
                maquina.say(f'A temperatura em São Paulo é de {
                            temperatura} graus Celsius.')
                maquina.runAndWait()

    else:
        pass


while True:
    execute_command()

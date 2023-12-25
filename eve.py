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
import webbrowser


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

# Função para abrir o site


def open_site():
    url = "https://aluno.uninove.br/seu/CENTRAL/aluno/"
    # Abre a página em uma nova guia do Microsoft Edge
    webbrowser.open(url, new=1)


audio = sr.Recognizer()
maquina = pyttsx3.init()


def transcribe_and_save():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Transcrevendo...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        transcript = recognizer.recognize_google(audio, language="pt-BR")
        print("Transcrição: " + transcript)

        # Obter a data e hora atual
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Salvar a transcrição no arquivo .txt
        with open("transcriptions.txt", "a") as file:
            file.write(f"{current_datetime} - {transcript}\n")

    except sr.UnknownValueError:
        print("Não foi possível transcrever o que você disse.")

    except sr.RequestError as e:
        print(
            f"Não foi possível conectar ao serviço de reconhecimento de voz; {e}")
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

            elif 'abra o site do aluno' in comando:
                maquina.say('Abrindo o site')
                maquina.runAndWait()
                open_site()

            elif 'toque' in comando:
                musica = comando.replace('toque', '')
                resultado = pywhatkit.playonyt(musica)
                maquina.say(f'Tocando {musica} no youtube')
                maquina.runAndWait()

            elif 'está por aí' in comando:
                maquina.say('Olá senhor, o que precisa"?')
                maquina.runAndWait()

            elif 'transcreva' in comando:
                transcribe_and_save()
                maquina.say(comando)
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

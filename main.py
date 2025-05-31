"""
ai_assistant.py
A voice-activated AI assistant that wakes on the phrase “hello jarvis”.

Dependencies
------------
pip install speechrecognition pyttsx3 pyaudio openai

Notes
-----
• Set OPENAI_API_KEY in your environment first.
• On Windows you may need to download PortAudio binaries for pyaudio.
"""

import time, speech_recognition as sr, pyttsx3,openai
import eel, os
from openai.error import OpenAIError
from engine.features import *
from engine.pycache.command import speak
from engine.auth.trainer import recoganize
"""
WAKE_WORD = "hello"
openai.api_key = os.getenv("OPENAI_API_KEY")          # export OPENAI_API_KEY=...

# ---------- Text-to-speech ---------- #
engine = pyttsx3.init()
def speak(text: str) -> None:
    #Say something aloud and also print it to console.
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

# ---------- Speech-to-text ---------- #
def transcribe(recognizer: sr.Recognizer, audio: sr.AudioData) -> str:
    #Return lowercase text or empty string if not understood.
    try:
        return recognizer.recognize_google(audio).lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print(f"[Google SR error] {e}")
        return ""

def listen(recognizer: sr.Recognizer, mic: sr.Microphone,
           limit: int | None = None) -> str:
    #Capture audio from the mic, return transcribed text.
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        audio = recognizer.listen(source, phrase_time_limit=limit)
    
    return transcribe(recognizer, audio)

# ---------- OpenAI chat ---------- #
SYSTEM_PROMPT = "You are a helpful AI assistant named Jarvis."
def ask_openai(prompt: str, chat_log: list[dict]) -> str:
    #Send user prompt + history to OpenAI and return the assistant reply.
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for turn in chat_log:
            messages += [
                {"role": "user", "content": turn['user']},
                {"role": "assistant", "content": turn['assistant']}
            ]
        messages.append({"role": "user", "content": prompt})

        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        return resp.choices[0].message.content.strip()
    except OpenAIError as e:
        print(f"[OpenAI error] {e}")
        return "Seems like the device is offline....."

# ---------- Main loops ---------- #
def conversation(recognizer: sr.Recognizer, mic: sr.Microphone) -> None:
    #Hold a voice conversation until the user says 'stop' / 'exit'.
    chat_log: list[dict] = []
    while True:
        user_input = listen(recognizer, mic, limit=10)
        if not user_input:           # silence / noise
            continue
        print(f"You: {user_input}")

        if user_input in {"stop", "exit", "goodbye"}:
            speak("Good-bye!")
            break

        if user_input in {"shutdown"}:
            speak("Shutting down...")
            exit()

        reply = ask_openai(user_input, chat_log)
        chat_log.append({"user": user_input, "assistant": reply})
        speak(reply)

def wake_word_listener() -> None:
    recognizer, mic = sr.Recognizer(), sr.Microphone()
    speak(f"Assistant online. Say “{WAKE_WORD}” to wake me.")
    while True:
        print("Listening for wake word...")
        text = listen(recognizer, mic, limit=3)
        if WAKE_WORD in text:
            
            eel.init("www")
            os.system('start msedge.exe --app="http://localhost:8000/index.html"')
            eel.start('index.html', mode=None, host='localhost', block=True)
            speak("Hello There")
            conversation(recognizer, mic)


if __name__ == "__main__":
    try:
        wake_word_listener()
    except KeyboardInterrupt:
        print("\n[Interrupted]")
"""

def start():

    eel.init("www")

    @eel.expose
    def init():
        eel.hideLoader()
        speak("Initializing Face Authentication")
        flag = recoganize.AuthenticateFace()
        if flag == 1:
            #subprocess.call([r'device.bat'])
            eel.hideFaceAuth()
            speak("Face Authentication Successfull")
            speak("ID verfied")
            eel.hideFaceAuthSuccess()
            speak("Welcome Sir.")
            eel.hideStart()
            playAssistantSound()
        else:
            speak("Face Authentication Failed")

    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    eel.start('index.html', mode=None, host='localhost', block=True)
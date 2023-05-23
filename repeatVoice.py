import speech_recognition as sr
# import pyttsx3
import voicevox

r = sr.Recognizer()
# engine = pyttsx3.init()

with sr.Microphone() as source:
    print("話しかけてください:")
    audio = r.listen(source)

try:
    text = r.recognize_google(audio, language="ja-JP")
    print("認識結果:", text)
    voicevox.text_to_speech(text, 3)
    # engine.say(text)
    # engine.runAndWait()
except sr.UnknownValueError:
    print("音声が認識できませんでした")
except sr.RequestError:
    print("サービスにアクセスできませんでした")
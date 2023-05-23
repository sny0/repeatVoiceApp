import speech_recognition as sr
# import pyttsx3
import voicevox

input_time = 20 # 入力時間[s]
r = sr.Recognizer()
# engine = pyttsx3.init()

with sr.Microphone() as source:
    print("話しかけてください:")
    audio = r.listen(source, input_time)
    print("認識中です・・・")

try:
    text = r.recognize_google(audio, language="ja-JP")
    print("認識結果:", text)
    voicevox.text_to_speech(text, 38) # 第二引数でキャラクタを指定（参考：https://happy-shibusawake.com/voicevox_engine/1004/
    # engine.say(text)
    # engine.runAndWait()
except sr.UnknownValueError:
    print("音声が認識できませんでした")
except sr.RequestError:
    print("サービスにアクセスできませんでした")
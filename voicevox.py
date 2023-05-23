import requests
import json
import time
import re
import simpleaudio

#参考：https://note.com/mega_gorilla/n/n8cec1ce5ccaa

file_path = './audio.wav'  # 保存先のファイルパス

def save_audio_file(audio_data, file_path):
    with open(file_path, 'wb') as file:
        file.write(audio_data)

def audio_query(text, speaker, max_retry):
    # 音声合成用のクエリを作成する
    query_payload = {"text": text, "speaker": speaker}
    for query_i in range(max_retry):
        r = requests.post("http://localhost:50021/audio_query", 
                        params=query_payload, timeout=(10.0, 300.0))
        if r.status_code == 200:
            query_data = r.json()
            time.sleep(1)
            break
        else:
            raise ConnectionError("リトライ回数が上限に到達しました。 audio_query : ", "/", text[:30], r.text)
    return query_data
def synthesis(speaker, query_data,max_retry):
    synth_payload = {"speaker": speaker}
    for synth_i in range(max_retry):
        r = requests.post("http://localhost:50021/synthesis", params=synth_payload, 
                          data=json.dumps(query_data), timeout=(10.0, 300.0))
        if r.status_code == 200:
            #音声ファイルを返す
            return r.content
        else:
            raise ConnectionError("音声エラー：リトライ回数が上限に到達しました。 synthesis : ", r)


def text_to_speech(texts, speaker=8, max_retry=20):
    print(texts)
    if texts==False:
        texts="ちょっと、通信状態悪いかも？"
    texts=re.split("(?<=！|。|？)",texts)
    play_obj=None
    for text in texts:
        # audio_query
        query_data = audio_query(text,speaker,max_retry)
        print(query_data)
        # synthesis
        voice_data=synthesis(speaker,query_data,max_retry)
        save_audio_file(voice_data, file_path)
        #音声の再生
        if play_obj != None and play_obj.is_playing():
            play_obj.wait_done()
        # WAVファイルを読み込む
        wave_obj = simpleaudio.WaveObject.from_wave_file(file_path)

        # WAVファイルを再生する
        play_obj = wave_obj.play()

        # 再生が終了するまで待機する
        play_obj.wait_done()

if __name__ == "__main__": 
    print("main")
    text_to_speech("こんにちは、ずんだもんなのだ", 3)
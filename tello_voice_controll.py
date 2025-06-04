import socket
import sys
import json
import queue
import threading
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# ===============================
# 設定
# ===============================
UDP_IP = "192.168.10.1"  # TelloのIP
UDP_PORT = 8889          # コマンドポート
LOCAL_PORT = 9000        # 自分側の受信ポート
MODEL_PATH = "vosk-model"  # Voskモデルパス（事前に展開しておく）

# ===============================
# 音声認識 初期化
# ===============================
q = queue.Queue()
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)

# ===============================
# UDP通信 初期化
# ===============================
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', LOCAL_PORT))

# SDKモードへ（これを送らないとTelloが無反応）
sock.sendto(b'command', (UDP_IP, UDP_PORT))
print("✅ Telloに 'command' を送信しました")

# ===============================
# 応答受信スレッド
# ===============================
def receive():
    while True:
        try:
            response, _ = sock.recvfrom(1024)
            print(f"📥 ドローン応答: {response.decode('utf-8')}")
        except Exception as e:
            print(f"❌ 応答エラー: {str(e)}")
            break

recv_thread = threading.Thread(target=receive, daemon=True)
recv_thread.start()

# ===============================
# 音声入力コールバック
# ===============================
def callback(indata, frames, time, status):
    if status:
        print(f"⚠️ 音声入力ステータス: {status}", file=sys.stderr)
    q.put(bytes(indata))

# ===============================
# 音声→ドローンコマンド解釈
# ===============================
def interpret_command(text):
    if "離陸" in text or "テイクオフ" in text:
        return "takeoff"
    elif "着陸" in text or "ランディング" in text:
        return "land"
    elif "前" in text:
        return "forward 20"
    elif "後ろ" in text:
        return "back 20"
    elif "右" in text:
        return "right 20"
    elif "左" in text:
        return "left 20"
    elif "上" in text:
        return "up 20"
    elif "下" in text:
        return "down 20"
    elif "回れ" in text or "旋回" in text:
        return "cw 90"
    elif "止まれ" in text or "ストップ" in text:
        return "stop"
    return None

# ===============================
# メインループ
# ===============================
def main():
    print("🎤 音声認識開始！Ctrl+Cで終了")
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                print(f"🗣 認識結果: {text}")
                command = interpret_command(text)
                if command:
                    print(f"✈️ 送信コマンド: {command}")
                    sock.sendto(command.encode(), (UDP_IP, UDP_PORT))

# ===============================
# エントリーポイント
# ===============================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 終了します。")

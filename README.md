#音声認識ドローン操作プログラム

## 概要
音声認識を用いてドローンを操作するプログラムです。音声コマンドを解析し、ドローンの動作を制御します。<p>
音声コマンドを認識するモデルは、voskの音声認識モデル(計量版若しくはフル版)を使用します。<p>
https://alphacephei.com/vosk/models<br>
上記リンクよりダウンロードしてください。
## 必要なライブラリ(requirements.txt)
以下のライブラリが必要です。<br>
- vosk
- pyaudio
- dronekit
- opencv-python
- numpy
- pyserial
- pyttsx3

##動作環境
Windows 10以上<br>
python 3.12以上<br>
## インストール方法
1. 適当なディレクトリにクローンします。
   ```bash
   git clone
   ```
2. 必要なライブラリをインストールします。
   ```bash
    python -m venv .venv
    source .venv/bin/activate # Windowsなら .venv\Scripts\activate
    pip install -r requirements.txt
   ```
3. 音声認識モデルをダウンロードし、`vosk-model`ディレクトリに配置します。
   ```bash
    mkdir vosk-model
    # vosk-modelディレクトリに音声認識モデルを配置
    # 例: vosk-model/vosk-model-small-ja-0.22
    # または vosk-model/vosk-model-ja-0.22
    # どちらか一方を配置してください。
    ```
4. ドローンの電源を起動し、コンピュータのWifiをドローンに接続します。
5. 実行します。
   ```bash
   python main.py
   ```
## トラブルシューティング
- 音声認識モデルが正しく配置されていない場合、`vosk-model`ディレクトリに音声認識モデルを配置してください。
- ドローンが正しく接続されていない場合、ドローンの電源を確認し、Wifi接続を確認してください。
- 音声認識がうまくいかない場合、マイクの設定を確認してください。
- 音声認識モデルのバージョンが古い場合、最新のモデルをダウンロードしてください。
- PyAudioでエラーが出るとき
    ```bash
    #Windows
    pip install pipwin
    pipwin install pyaudio
    #MacOS
    brew install portaudio
    pip install pyaudio
    #Linux
    sudo apt-get install python3-pyaudio
    ```

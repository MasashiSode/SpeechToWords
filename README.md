# SpeechToWords

## pythonモジュールのインストール関連

2019.02.20 Masashi Sode

**SpeechToWiki**

言葉から単語を抽出し，wikiのリンクを得るモジュール

- [wikipedia](https://pypi.org/project/wikipedia/)
- [pydub](https://github.com/jiaaro/pydub) *
- [MeCab](http://taku910.github.io/mecab/) *
- [google speech-to-text](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries) *

---

## SpeechToWiki

### wikipedia
[wikipedia api](https://pypi.org/project/wikipedia/)
```
pip install wikipedia
```

### pydub

pydub単体でも動くが，ffmpegが音声抽出に必要となるため，condaでインストールする．
conda以外の環境では，ffmpegをコンパイルする必要があるため，面倒です．

ffmpeg自体はもともとPythonのモジュールではなくソフトウェアです．
condaに配布されているのがこれを他のモジュールから呼び出せるようにバイナリ化されたものです．
ffmpegを環境ごとにコンパイルしていれるのが面倒なためcondaを選択しました．

**ffmpegは必ずcondaを使用してインストールしてください**

```
pip install pydub
conda install -c menpo ffmpeg
```

### MeCab

win 64 bit

[Windows10(64bit)でMeCab-Pythonを使えるようにするシンプルな方法（2018/6）Qiita](https://qiita.com/fu23/items/34f55f0b7aaa7e2205b8)

Ubuntu (未確認)

[ubuntu 18.04 に mecab をインストール](https://qiita.com/ekzemplaro/items/c98c7f6698f130b55d53)

### google speech to text

pipでAPIを操作するモジュールをインストール
```
pip install google-cloud
```
その後，以下の内容にそって，apiを有効にし，api keyを取得し，jsonファイルにパス 
を通す．

    Note:
        At first, follow the instruction written in
        https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries
        and prepare your environment to use Google Cloud.

        apiのキーを発行し，GOOGLE_APPICATION_CREDENTIALSにjsonファイルのパスを通すこと．
        https://cloud.google.com/docs/authentication/getting-started

        win
        $env:GOOGLE_APPLICATION_CREDENTIALS="PATH\TO\YOUR\[FILE_NAME].json"

        linux
        export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/[FILE_NAME].json"

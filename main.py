from lib.SoundRecorder import Recorder
from lib.Converter import Converter
from lib.SpeechToText import SpeechToText
from lib.TextToWords import TextToWords
from lib.WordToWiki import WordToWiki
from io import BytesIO, StringIO
import os

if __name__ == '__main__':
    audio_file = os.path.join('files', 'Audio20180930.raw')
    # audio_file = os.path.join('files', 'test.mkv')

    audio_file_wav = os.path.join('files', 'test.wav')
    text_file = 'text_data'
    link_file = 'link.dat'
    Rec = Recorder()
    Rec.set_rec_time(15)
    Rec.set_export_file(audio_file)
    Rec.setup()

    Rec.record()
    Rec.export_data()

# ----
    # Conv = Converter()
    # Conv.export_audio_file(audio_format='wav', export_path=audio_file_wav)
    Conv = Converter()
    Conv.import_audio_file(audio_format='raw', import_path=audio_file)
    # Conv.import_audio_file(audio_format='mkv', import_path=audio_file)
    f = Conv.export_audio(audio_format='wav')
    # Conv.export_audio_file(audio_format='wav', export_path=audio_file_wav)

# # ----
    STT = SpeechToText()

    # import the audio file.
    # print(StringIO(f))
    STT.read_audio(f)
    # STT.read_audio_file(file_name=audio_file_wav)

    # set the language code in the audio file.
    # STT.SetLanguageCode('en-US')
    STT.set_language_code('ja-JP')
    # print(STT.audio)

    # run the entire code to request.
    STT.run()

    # export the text file
    STT.export_script(data_format='txt', export_file=text_file)
    txt = STT.export_txt_data()

# # ----

    TTW = TextToWords()
    # TTW.import_text_data(text_file + '.txt')
    TTW.import_str_data(txt)
    TTW.parse()
    TTW.extract_noun_words()
    print(TTW.noun_words.unique())

# # ---

    WTW = WordToWiki()
    WTW.search(TTW.noun_words.unique())
    WTW.export_to_text_file(link_file)

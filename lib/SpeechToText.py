import io
import os
import csv
import traceback
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


class SpeechToText():
    """
    2018.09.26 made by Masashi Sode

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

    Examples::

        file_name = os.path.join(
            os.path.dirname(__file__),
            'audio.raw')

        STT = SpeechToText()

        # import the audio file.
        STT.read_audio_file(file_name)

        # set the language code in the audio file.
        STT.set_language_code('en-US')
        # STT.set_language_code('ja-JP')

        # run the entire code to request.
        STT.run()

        # export the text file
        STT.export_script(format='csv', export_file='SpeechToText')
    """

    def __init__(self, audio_file_name=None):
        self.client = speech.SpeechClient()
        self.audio = None
        self.response = None
        self.audio_file_name = audio_file_name
        self.language_code = 'en-US'

        if audio_file_name is not None:
            try:
                self.read_audio_file(self.audio_file_name)
            except:
                raise ValueError

    def read_audio_file(self, file_name):
        """
        Loads the audio into memory
        """
        with io.open(file_name, 'rb') as audio_file:
            content = audio_file.read()
            self.audio = types.RecognitionAudio(content=content)

    def read_audio(self, file):
        """
        Loads the audio into memory
        """
        # with io.open(file_name, 'rb') as audio_file:
        content = file
        self.audio = types.RecognitionAudio(content=content)

    def set_language_code(self, language_code):
        """
        supported languages are listed in this website.
        https://cloud.google.com/speech-to-text/docs/languages

        usage:
        # English
        STT.set_language_code('en-US')
        # Japanese
        STT.set_language_code('ja-JP')
        """
        self.language_code = language_code

    def run(self):
        """
        run the entire code to request.
        """

        config = types.RecognitionConfig(
            # encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=self.language_code)
        # print(config)
        # Detects speech in the audio file
        self.response = self.client.recognize(config, self.audio)
        # print('-- run --')
        # print('response: ', self.response)
        # print('-- run --')

    def export_script(self, data_format='txt', export_file='SpeechToText'):
        """
        export_script
            exports the script file.
            data_format (str, optional): Defaults to 'txt'.
            export_file (str, optional): Defaults to 'SpeechToText'.

        Raises:
            ValueError: if data_format is not 'txt' or 'csv'
        """

        if data_format == 'txt':
            ext = '.txt'
            export_file_name = export_file + ext

            i = 0
            out = [None] * len(self.response.results)
            for result in self.response.results:
                out[i] = result.alternatives[0].transcript

            with open(export_file_name, mode='w', encoding='utf-8') as file:
                file.writelines('\n'.join(out))

        elif data_format == 'csv':
            ext = '.csv'
            export_file_name = export_file + ext

            i = 0
            out = [None] * len(self.response.results)
            for result in self.response.results:
                out[i] = result.alternatives[0].transcript.split()

            with open(export_file_name, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, lineterminator='\n')
                writer.writerows(out)

        else:
            traceback.print_exc()
            raise ValueError

    def export_txt(self, data_format='txt', export_file='SpeechToText'):
        """
        export_script
            exports the script file.
            data_format (str, optional): Defaults to 'txt'.
            export_file (str, optional): Defaults to 'SpeechToText'.

        Raises:
            ValueError: if data_format is not 'txt' or 'csv'
        """

        if data_format == 'txt':
            ext = '.txt'
            export_file_name = export_file + ext

            i = 0
            out = [None] * len(self.response.results)
            for result in self.response.results:
                out[i] = result.alternatives[0].transcript

            with open(export_file_name, mode='w', encoding='utf-8') as file:
                txt = '\n'.join(out)
                file.writelines(txt)
                return txt

        elif data_format == 'csv':
            ext = '.csv'
            export_file_name = export_file + ext

            i = 0
            out = [None] * len(self.response.results)
            for result in self.response.results:
                out[i] = result.alternatives[0].transcript.split()

            with open(export_file_name, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, lineterminator='\n')
                writer.writerows(out)
                return out

        else:
            traceback.print_exc()
            raise ValueError

    def export_txt_data(self):
        i = 0
        out = [None] * len(self.response.results)
        for result in self.response.results:
            out[i] = result.alternatives[0].transcript
        txt = '\n'.join(out)
        return txt


if __name__ == '__main__':
    FILE_NAME = os.path.join(
        os.path.dirname(__file__),
        'output.raw')
    STT = SpeechToText()

    # import the audio file.
    STT.read_audio_file(FILE_NAME)

    # set the language code in the audio file.
    # STT.set_language_code('en-US')
    STT.set_language_code('ja-JP')

    # run the entire code to request.
    STT.run()

    # export the text file
    STT.export_script(data_format='csv', export_file='SpeechToText')

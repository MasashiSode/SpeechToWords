from pydub import AudioSegment
from io import StringIO, BytesIO
import io


class Converter(object):
    """
    2018.09.28 made by Masashi Sode

    Examples::

        Conv = Converter()
        Conv.import_audio_file(format='raw', ImportPath='test.raw')
        Conv.export_audio_file(format='wav', ExportPath='test.wav')

    """

    def __init__(self):
        self.audio = None
        self.sample_width = 2
        self.frame_rate = None
        self.channels = 1

    def import_audio_file(self, audio_format=None, import_path=None):
        if audio_format == 'raw':
            self.frame_rate = 16000
            self.audio = AudioSegment.from_raw(
                import_path,
                sample_width=self.sample_width,
                frame_rate=self.frame_rate,
                channels=self.channels)

        elif audio_format == 'wav':
            self.frame_rate = 44100
            self.audio = AudioSegment.from_wav(
                import_path,
                sample_width=self.sample_width,
                frame_rate=self.frame_rate,
                channels=self.channels)

        elif audio_format == 'mp3':
            self.frame_rate = 44100
            self.audio = AudioSegment.from_mp3(
                import_path,
                sample_width=self.sample_width,
                frame_rate=self.frame_rate,
                channels=self.channels)
        elif audio_format == 'mkv':
            # self.frame_rate = 44100
            self.audio = AudioSegment.from_file(import_path)
        else:
            raise ValueError
        return

    def import_audio(self, import_data=None):
        # self.frame_rate = 44100
        file = BytesIO(import_data)
        sample_width = 4
        channels = 1
        frame_rate = 48000
        self.audio = AudioSegment.from_file(file,
            sample_width=sample_width,
            channels=channels,
            frame_rate=frame_rate)
        return

    def export_audio_file(self, audio_format='raw', export_path=None):
        """
        format = 'raw', 'wav' or 'mp3'.
        """
        self.audio.export(export_path, format=audio_format)
        return

    def export_audio(self, audio_format='raw'):
        """
        format = 'raw', 'wav' or 'mp3'.
        """
        buf = io.BytesIO()
        temp = self.audio
        temp = self.audio.set_frame_rate(16000)
        temp = temp.set_sample_width(2)
        temp.export(buf, format=audio_format)
        # temp.export('test.wav', format=audio_format)
        # print('test audio exported')
        duration = temp.duration_seconds
        return buf.getvalue(), duration

if __name__ == '__main__':
    Conv = Converter()
    Conv.import_audio_file(format='raw', import_path='output.raw')
    Conv.export_audio_file(format='wav', export_path='output.wav')

import wave
import pyaudio


class Recorder():
    """
    Examples::

        Rec = Recorder()

        # setup record parameters
        Rec.set_rec_time(5)
        Rec.set_export_file('test.raw')
        Rec.setup()

        Rec.record()
        Rec.export_data()
    """

    def __init__(self):
        self.rec_time = 10
        self.export_file = 'output.raw'
        self.fmt = pyaudio.paInt16  # 音声のフォーマット
        self.channel = 1
        self.sampling_rate = 16000  # サンプリング周波数
        self.chunk = int(self.sampling_rate / 10)    # チャンク（データ点数）
        self.audio = pyaudio.PyAudio()
        self.index = 1
        self.frames = []
        self.wav = None
        self.stream = None

    def set_export_file(self, export_file_path):
        """
        set_export_file [summary]

        Args:
            export_file_path (str): file path of the exported sound file
        """

        self.export_file = export_file_path

    def set_sampling_rate(self, sampling_rate=16000):
        """
        set_sampling_rate [summary]

        Args:
            sampling_rate (int, optional): Defaults to 16000.
        """

        self.sampling_rate = sampling_rate
        self.chunk = int(self.sampling_rate / 10)

    def set_rec_time(self, rec_time=10):
        """
        set_rec_time [summary]

        Args:
            rec_time (int, optional): Defaults to 10.
        """

        self.rec_time = rec_time

    def setup(self):
        """
        set up stream data
        """

        self.stream = self.audio.open(format=self.fmt, channels=self.channel,
                                      rate=self.sampling_rate, input=True,
                                      input_device_index=self.index,
                                      frames_per_buffer=self.chunk)

    def record(self):
        """
        records sound
        """

        # 録音処理
        print("recording start...")
        self.frames = []
        for i in range(0, int(self.sampling_rate / self.chunk * self.rec_time)):
            data = self.stream.read(self.chunk)
            self.frames.append(data)

        # 録音終了処理
        print("recording  end...")
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def export_data(self):
        """
        export_data 録音データをファイルに保存
        """

        self.wav = wave.open(self.export_file, 'wb')
        self.wav.setnchannels(self.channel)
        self.wav.setsampwidth(self.audio.get_sample_size(self.fmt))
        self.wav.setframerate(self.sampling_rate)
        self.wav.writeframes(b''.join(self.frames))
        self.wav.close()


if __name__ == '__main__':
    Rec = Recorder()

    Rec.set_rec_time(5)
    Rec.set_export_file('output.raw')
    Rec.setup()

    Rec.record()
    Rec.export_data()

import sys
from io import StringIO
import MeCab
# import re
import pandas as pd


class TextToWords():
    """TextToWords テキストデータから名詞を抽出するクラス
    MeCabは https://qiita.com/fu23/items/34f55f0b7aaa7e2205b8 を参考に導入した．
    """

    def __init__(self):
        self.text = None
        self.parsed_data = None
        self.mecab = MeCab.Tagger("-Ochasen")
        self.df = pd.DataFrame()

    def import_text_data(self, file_path):
        """import_text_data テキストファイルをクラス内に取り込むときに使用するメソッド

        Args:
            file_path (str): MeCabに解析させたい文字列データの記録されたテキストファイル
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            self.text = file.read()

    def import_str_data(self, str_data):
        """import_str_data 文字列データをクラスに取り込むときに使用するメソッド

        Args:
            str_data (str): MeCabに解析させたい文字列データ
        """

        self.text = str_data

    def parse(self):
        """
        parse MeCabによる形態素解析を行って結果をpandasのDataFrameに格納するメソッド
        """

        self.parsed_data = self.mecab.parse(self.text)
        TESTDATA = StringIO(self.parsed_data)
        self.df = pd.read_csv(TESTDATA, sep='\t', header=None)
        self.df = self.df[self.df.iloc[:, 0] != 'EOS']

    def extract_noun_words(self):
        """extract_noun_words
        pandasのDataFrameを使用して名詞のみを取り出すメソッド
        self.noun_wordsにpandasのSeriesとして名詞のデータを格納する．
        後々の頻度解析などに必要なため名詞の重複は処理されずにそのまま格納される．

        """
        # self.noun_words = \
        #     self.df[('名詞' in self.df.iloc[:, 3] ==
        #              '名詞-一般') | (self.df.iloc[:, 3] == '名詞-サ変接続')].iloc[:, 0]
        if len(self.df.index) == 0:
            self.noun_words = pd.DataFrame()
        else:
            self.noun_words = \
                self.df[(self.df.iloc[:, 3].str.contains('名詞')) & ~(
                    self.df.iloc[:, 3].str.contains('代名詞')) & ~(
                    self.df.iloc[:, 3].str.contains('非自立'))].iloc[:, 0]
        return self.noun_words


if __name__ == "__main__":
    txt_file = 'test_data.txt'
    TTW = TextToWords()
    TTW.import_text_data(txt_file)
    TTW.parse()
    TTW.extract_noun_words()
    print(TTW.noun_words)
    # print(TTW.df)
    # print(TTW.df.iloc[:, 3].str.contains('名詞'))

import sys
from io import StringIO
import MeCab
# import re
import pandas as pd
import numpy as np


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
        test_data = StringIO(self.parsed_data)
        self.df = pd.read_csv(test_data, sep='\t', header=None)
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
            temp = self.noun_words.index[1:] - self.noun_words.index[:-1]
            temp = np.append(temp, [0])
            # print(temp)
            index = self.noun_words.index[temp == 1]
            index_next = index + 1
            # print(index, index_next)
            self.idiom = pd.Series(self.noun_words[index].values +
                                   self.noun_words[index_next].values)

            index_long_words = [False] * len(self.noun_words.tolist())
            for i, char in enumerate(self.noun_words.tolist()):
                index_long_words[i] = len(char) >= 4
            self.long_words = self.noun_words[index_long_words]

            self.difficult_words = pd.Series(self.idiom.tolist() + self.long_words.tolist())

            self.noun_words_with_idiom = pd.Series(self.noun_words.tolist() + self.idiom.tolist())
        return self.noun_words_with_idiom

if __name__ == "__main__":
    import string

    txt_file = 'test_data.txt'
    TTW = TextToWords()
    TTW.import_text_data(txt_file)
    TTW.parse()
    print(TTW.extract_noun_words())
    # print(TTW.noun_words)

    temp = TTW.noun_words.index[1:] - TTW.noun_words.index[:-1]
    temp = np.append(temp, [0])
    # print(temp)
    index = TTW.noun_words.index[temp == 1]
    index_next = index + 1
    # print(index, index_next)
    out = TTW.noun_words[index].values + TTW.noun_words[index_next].values

    # TTW.noun_words[index] = out
    # print()

    # print([chr(i) for i in range(12449, 12532+1)])
    # print(TTW.noun_words[index_next])

    # import re
    # # 全て全角カタカナか？
    # # Pythonの正規表現で、渡された文字列が全てASCII文字かチェックします。(UTF-8向け)
    # # Python 正規表現 ASCII文字 UTF8
    # regexp = re.compile(r'^(?:\xE3\x82[\xA1-\xBF]|\xE3\x83[\x80-\xB6])+$')
    # # a = "カタカナ"
    # # print(a)
    # for i, char in enumerate(TTW.noun_words.tolist()):
    #     print(len(char) > 4)
        # result = regexp.search(char)
        # print(char, result)

        # if result != None:
        #     print(u"すべてが全角カタカナである")
        # else:
        #     print(u"すべてが全角カタカナではない")

    # j = 0
    # for i in TTW.noun_words.index:
    #     if i:
    #         pass

    # print(TTW.df)
    # print(TTW.df.iloc[:, 3].str.contains('名詞'))

import wikipedia
import requests
import numpy as np


class WordToWiki():
    def __init__(self):
        wikipedia.set_lang("jp")
        self.url = 'https://www.google.co.jp/search'

    def set_lang(self, lang='jp'):
        wikipedia.set_lang(lang)

    def search(self, words):
        self.words = words
        if type(words) in (list, np.ndarray):
            self.wiki_url = [None] * len(words)
            for i, word in enumerate(words):
                try:
                    self.wiki_url[i] = wikipedia.page(word).url

                except wikipedia.exceptions.DisambiguationError as e:
                    self.wiki_url[i] = wikipedia.page(e.options[0]).url

                except wikipedia.exceptions.PageError as e:
                    req = requests.get(self.url, params={'q': word})
                    self.wiki_url[i] = req.url
                except wikipedia.exceptions.DisambiguationError as e:
                    req = requests.get(self.url, params={'q': word})
                    self.wiki_url[i] = req.url
        else:
            try:
                self.wiki_url = wikipedia.page(words).url

            except wikipedia.exceptions.DisambiguationError as e:
                self.wiki_url = wikipedia.page(e.options[0]).url

            except wikipedia.exceptions.PageError as e:
                req = requests.get(self.url, params={'q': words})
                self.wiki_url = req.url
        return self.wiki_url

    def export_to_text_file(self, output_file):
        with open(output_file, 'w', encoding='utf-8') as file:
            if type(self.wiki_url) in (list, np.ndarray):
                for i, item in enumerate(self.wiki_url):
                    file.write("{w} : {im}\n".format(w=self.words[i], im=item))
            else:
                file.write("{w} : {im}\n".format(
                    w=self.words, im=self.wiki_url))


if __name__ == "__main__":
    word = ['現在', 'WBS', '関数', 'テスト']
    WTW = WordToWiki()

    WTW.search(word)
    WTW.export_to_text_file('test.dat')

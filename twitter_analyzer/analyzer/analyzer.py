import numpy as np
import nltk
import glob
import csv
import os

from matplotlib import pyplot as plt

from nltk.stem import LancasterStemmer
from stop_words import get_stop_words


class Analyzer:
    def __init__(self, file_path):
        """Search and load processed .npy file first, if not found, open csv and do processing"""
        self.file_name = os.path.basename(file_path)
        self.file_path = file_path
        self.data_dir = 'data_files'
        os.makedirs(self.data_dir, exist_ok=True)
        data = self.load_data()

        if data is not None:
            self.data = data
        else:
            self.preprocess()

    def preprocess(self):
        print(f"Preprocessing: {self.file_name}")
        self.data = self.tokenize_file(self.file_path)
        self.normalize_text(self.data)
        self.remove_polish_letters(self.data)
        self.stemming(self.data, 'polish')
        self.drop_short_words(self.data)

    @staticmethod
    def tokenize_file(absolute_file_path):
        with open(absolute_file_path, 'rt') as file:
            rider = csv.reader(file, delimiter=',')
            data = []
            tt = nltk.tokenize.TweetTokenizer(strip_handles=True, reduce_len=True, preserve_case=False)
            for index, row in enumerate(rider):
                text = row[-1]
                if index == 0:
                    header = text
                    continue

                if text.startswith('RT'):
                    continue
                else:
                    text = Analyzer.remove_symbols(text)
                    token = tt.tokenize(text)
                    data.append((row[2], token))

            data = np.array(data)
            return data

    @staticmethod
    def remove_symbols(text):
        symbs = ['-', '_', '=', '.', '#']
        for sym in symbs:
            text = text.replace(sym, '')
        return text

    @staticmethod
    def remove_polish_letters(data_array: 'list <index, text>'):
        """Function will replace polish letters in data object"""
        letters = {'ą': 'a', 'ć': 'c', 'ę': 'e', 'ó': 'o', 'ł': 'l',
                   'ń': 'n', 'ś': 's', 'ż': 'z', 'ź': 'z'}
        for pair in data_array:
            words = pair[1]
            for ind, wrd in enumerate(words):
                for pl, normal in letters.items():
                    wrd = wrd.replace(pl, normal)
                pair[1][ind] = wrd

    @staticmethod
    def normalize_text(data_array: 'list of pair <index, text>'):
        """
        Remove stop words, and symbols. Remove every word shorter than min_word_len
        Args:
            data_array:
            min_word_len: int, default 2

        Returns:

        """
        stop_words = get_stop_words('polish')
        banned_symbols = [':', '"', "'", '.', '`', '”', '„', '/']
        banned_prefix = ['http']
        for pair in data_array:
            text = pair[1]
            # print(text)
            text = [word for word in text for pref in banned_prefix if
                    not word.startswith(pref) and word not in banned_symbols and word not in stop_words]
            pair[1] = text

    @staticmethod
    def drop_short_words(data_array: 'list of pair <index, text>', min_word_len=2):
        for pair in data_array:
            text = pair[1]
            # print(text)
            text = [word for word in text if len(word) >= min_word_len]
            pair[1] = text

    @staticmethod
    def stemming(data_array: 'list of pair <index, text>', lang=None):
        """
        Removes common prefixes and sufixes
        Args:
            list_array:

        Returns:

        """
        if lang == 'english' or lang is None:
            stemmer = LancasterStemmer()
            for pair in data_array:
                pair[1] = [stemmer.stem(word) for word in pair[1]]
        elif lang == 'polish':
            common_sufixes = ['bym',
                              'lam', 'lem', 'le', 'lo', 'li', 'iel', 'al',
                              'ja', 'yjna', 'yjnym',
                              'uja', 'uje', 'uje', 'uja', 'imi',
                              'ecie', 'ej', 'eria',
                              'iemy', 'iesz', 'emy', 'em', 'ie', 'ia', 'eni',
                              'kow', 'ko', 'ka', 'ke', 'ek',
                              'ac', 'amy', 'any', 'anie', 'a',
                              'acych', 'e',
                              'aj', 'ilem', 'u', 'ach', 'ch', 'om',
                              'ego',
                              'o', 'owi', 'owani', 'owy', 'owemu', 'owac', 'owym', 'owe', 'owie', 'ow',
                              'owny', 'ownosc',
                              'ym', 'emu',
                              'es', 'as',
                              'cie', 'ci', 'c',
                              'ami', 'ach', 'mi', 'im', 'in', 'i', 'y', 'uj']
            for pair in data_array:
                for sufix in common_sufixes:
                    pair[1] = [word if not word.endswith(sufix) else word[:-len(sufix)] for word in pair[1]]

    @staticmethod
    def lematizing(list_array: 'list of pair <index, text>'):
        """
        Converts words to basic form
        Args:
            list_array:

        Returns:

        """
        pass

    def load_data(self, file_name=None):
        if file_name is None:
            file_name = self.file_name
        try:
            data = np.load(os.path.join(self.data_dir, file_name + '.npy'), allow_pickle=True)
            print(f"Loaded data: {file_name}")
            return data
        except FileNotFoundError:
            print(f"Not found file: {file_name}")
            return None

    def save_data(self, file_name=None):
        if file_name is None:
            file_name = self.file_name
        if self.data is not None:
            np.save(os.path.join(self.data_dir, file_name), self.data)
            print(f"Saved file: {file_name}")

    def show(self, num):
        if num < 0:
            pass
        else:
            arr = np.random.randint(0, len(self.data), num)
            for x in arr:
                try:
                    print(f"{self.data[x, 0]}: {self.data[x, 1]}")
                except IndexError:
                    break

    # def word_bag(self):
    #     words = ['pis', 'duda', 'prezydent', 'wybory']

    def all_words(self):
        """Returns list of all unique words in this dataset"""
        all_words = []
        count = {}
        for pair in self.data:
            words = pair[1]
            for w in words:
                cur_count = count.get(w, 0)
                count.update({w: cur_count + 1})
            all_words += words
        all_words.sort()
        count = list(count.items())
        count.sort(key=lambda x: (x[0], x[1]), reverse=True)
        return all_words, count


if __name__ == '__main__':
    directory = os.path.join(
            os.path.dirname(os.path.dirname(
                    os.path.abspath(__file__))),
            'exports')

    all_files = glob.glob(os.path.join(directory, 'pl*.csv'), recursive=True)
    for file in all_files:
        print(file)

    app = Analyzer(file_path=all_files[-1])
    # app.preprocess()
    # app.show(10)
    all_words, count = app.all_words()

    # for key, value in count:
    #     if 0 < value <= 1:
    #         print(f"{value:<3} {key}")
    print(f"Word ammount: {len(count)}")
    app.save_data()

    import networkx as nx

    graf = nx.Graph()
    for x in range(1, 100):
        # graf.add_edges_from([(x, x + 1)])
        graf.add_edges_from([(x, x // 10)])

    A = graf.edges()
    for a in A:
        if 5 in a:
            print(a)

    B = nx.to_dict_of_lists(graf)
    print(B[5])

    plt.figure(figsize=(16, 9))
    nx.draw_networkx(graf)
    # plt.show()

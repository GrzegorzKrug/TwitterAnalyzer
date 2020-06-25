import numpy as np
import gensim
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
        self.model_dir = 'model_files'

        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.model_dir, exist_ok=True)

        data = self.load_data()
        lda = self.load_model()

        if data is not None:
            self.data = data
        else:
            self.preprocess()

        self.all_words, self.count = self.get_all_words()

        if lda is None:
            self.lda = None
            self.create_LDA_movel()
        else:
            self.lda = lda

    def preprocess(self):
        print(f"Preprocessing: {self.file_name}")
        self.data = self.tokenize_file(self.file_path)
        self.normalize_text(self.data)
        self.remove_polish_letters(self.data)
        self.stemming(self.data, 'polish')
        self.drop_useless_words(self.data, min_word_len=2)

    def create_LDA_movel(self):
        print("Creating LDA model")
        words = self.data[:, 1]
        dict = gensim.corpora.Dictionary(words)
        dict.filter_extremes(no_below=10, no_above=0.2)  # minimum 2 occuraces and no more than 20%
        bow = [dict.doc2bow(text) for text in words]

        lda = gensim.models.LdaMulticore(bow, num_topics=3, id2word=dict, passes=10, iterations=1000)
        self.lda = lda

    def drop_useless_words(self, data_array: 'list of pair <index, text>', min_word_len=2):
        """
        Drops short words, and very rare
        Args:
            data_array:
            min_word_len:

        Returns:

        """
        for pair in data_array:
            text = pair[1]

            text = [word for word in text if len(word) >= min_word_len]
            pair[1] = text

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

    def load_model(self):
        file_name = self.file_name
        try:
            full_path = os.path.join(self.model_dir, file_name)
            lda = gensim.models.LdaMulticore.load(full_path)
            print("Loaded model")
            return lda
        except FileNotFoundError:
            print(f"Not found this model: {file_name}")
            return None

    def save_model(self):
        file_name = self.file_name
        full_path = os.path.join(self.model_dir, file_name)
        self.lda.save(full_path)

        print(f"Saved model: {file_name}")

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
            print(f"Saved data: {file_name}")

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

    def get_all_words(self):
        """
        Returns:
            list of all words in this data set, duplicates can occur in list
            list - pair <word, number> sorted A..Z
        """
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
    # app.create_LDA_movel()
    # app.preprocess()
    # app.show(10)

    # count = app.count
    # for key, value in count:
    #     if 1000 < value <= 20000:
    #         print(f"{value:<3} {key}")
    # print(f"Word ammount: {len(count)}")
    a = app.lda.print_topic(-1)
    print(a)

    app.save_data()
    app.save_model()

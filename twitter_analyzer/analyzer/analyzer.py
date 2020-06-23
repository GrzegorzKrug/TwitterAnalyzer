import numpy as np
import nltk
import glob
import csv
import os

from nltk.stem import LancasterStemmer
from stop_words import get_stop_words


class Analyzer:
    def __init__(self, file_path):
        """Search and load processed .npy file first, if not found, open csv and do processing"""
        self.file_name = os.path.basename(file_path)
        self.data_dir = 'data_files'
        os.makedirs(self.data_dir, exist_ok=True)
        data = self.load_data()

        if data is not None:
            self.data = data
        else:
            self.data = self.tokenize_file(file_path)
            self.normalize_text(self.data)

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
                    token = tt.tokenize(text)
                    data.append((row[2], token))

            data = np.array(data)
            return data

    @staticmethod
    def normalize_text(list_array: 'list of pair <index, text>'):
        stop_words = get_stop_words('polish')
        banned_symbols = [':', '"', "'", '.', '`', '”', '„', '/']
        banned_prefix = ['http']
        for pair in list_array:
            text = pair[1]
            text = set(text)
            # print(text)
            text = [word for word in text for pref in banned_prefix if
                    not word.startswith(pref) and word not in banned_symbols and word not in stop_words
                    and len(word) > 0]
            pair[1] = text

    @staticmethod
    def stemming(list_array: 'list of pair <index, text>'):
        stemmer = LancasterStemmer()
        for pair in list_array:
            pair[1] = [stemmer.stem(word) for word in pair[1]]

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


if __name__ == '__main__':
    directory = os.path.join(
            os.path.dirname(os.path.dirname(
                    os.path.abspath(__file__))),
            'exports')

    all_files = glob.glob(os.path.join(directory, 'pl*.csv'), recursive=True)
    for file in all_files:
        print(file)

    app = Analyzer(file_path=all_files[-1])
    app.show(20)
    app.save_data()

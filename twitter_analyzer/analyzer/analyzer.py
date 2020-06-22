import numpy as np
import nltk
from nltk.stem import LancasterStemmer
import glob
import csv
import os


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
            pass

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
        banned_symbols = [':', '"', "'", '.']
        banned_prefix = ['http']
        for pair in list_array:
            text = pair[1]
            text = set(text)
            # print(text)
            text = [word for word in text for bn_pref in banned_prefix if
                    not word.startswith(bn_pref) and word not in banned_symbols]
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


if __name__ == '__main__':
    directory = os.path.join(
            os.path.dirname(os.path.dirname(
                    os.path.abspath(__file__))),
            'exports')

    all_files = glob.glob(os.path.join(directory, 'pl*.csv'), recursive=True)
    for file in all_files:
        print(file)

    app = Analyzer(file_path=all_files[-1])
    app.save_data()

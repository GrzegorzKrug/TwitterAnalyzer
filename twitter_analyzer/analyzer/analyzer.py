import numpy as np
import logging
import gensim
import nltk
import glob
import csv
import os
import re

from matplotlib import pyplot as plt

from nltk.stem import LancasterStemmer
from stop_words import get_stop_words


def mini_logger(name='analyzer'):
    logger = logging.getLogger(name=name)
    logger.setLevel('DEBUG')

    fh = logging.FileHandler('analyzer.log', mode='w')
    ch = logging.StreamHandler()

    # Log Formatting
    formatter = logging.Formatter(f'%(asctime)s - {name} - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.propagate = False

    return logger


class TextProcessor:
    """
    Processes text to `bag of words` (bow), works with text objects, and 2d lists [<id, text>]
    """

    def __init__(self, lang='polish'):
        self.lang = lang
        self.logger = mini_logger('text-processor')

    def full_preprocess(self, input_object):
        if type(input_object) is str:
            output = self.process_text(input_object)
        elif type(input_object) is list or type(input_object) is np.ndarray:
            if type(input_object[0, 0]) is str or type(input_object[0, 0] is np.str_):
                output = self.process_list(input_object)
            else:
                raise TypeError(f"Input type is unkown to TextProcessor: {type(input_object[0, 1])}")
        else:
            raise TypeError(f"Input type is unkown to TextProcessor: {type(input_object)}")
        return output

    def process_list(self, array):
        output = []
        for num, text in array:
            tokens = self.process_text(text)
            output.append([num, tokens])
            self.logger.debug(f"output: {num}, {tokens}")
        output = np.array(output)
        return output

    def process_text(self, text):
        text = text.lower()
        text = self.remove_polish_letters(text)
        tokens = self.tokenize_text(text)
        tokens = self.drop_useless_words(tokens)
        tokens = self.stemming(tokens)
        return tokens

    @staticmethod
    def drop_useless_words(tokens: 'list of strings'):
        """
        Drops short words, and very rare
        Args:
            data_array:
            min_word_len:

        Returns:

        """
        temp = tokens
        tokens = []
        for tk in temp:
            if len(tk) > 2:
                tokens.append(tk)
            elif len(tk) == 2 and tk.startswith("_"):
                tokens.append(tk)
        return tokens

    def tokenize_text(self, text):
        # self.logger.debug(f"Tokenizing: {text}")
        text = text.replace("’", " ")
        text = text.replace("'", " ")
        text = text.replace("“", " ")
        text = text.replace("”", " ")
        text = text.replace("„", " ")
        text = text.replace("\n", " ")
        text = text.replace(",", " ")
        text = text.replace("|", " ")

        # markers '!' '?' '...'
        text = re.sub(r'\?+', r' _q ', text)
        text = re.sub(r'\!+', r' _e ', text)
        text = re.sub(r'\.{3,}', ' _d ', text)

        # links and users mentions
        text = re.sub(r'(?<= )https((.*? )|(.*?$))', r' _l ', text)
        # text = re.sub(r'@\w+(?:(?: )|$)', r' _u ', text)

        # after hyperlinks
        text = text.replace("-", " ")
        text = text.replace("+", " ")
        text = text.replace("=", " ")
        text = text.replace('.', ' ')
        text = text.replace("\"", " ")

        # xd tags
        text = re.sub(r'[😂🤣😅]+', r' _x ', text)
        text = re.sub(r' ((x+d+ )|(x+d+$)|(x+p+ )|(x+p+$))', r' _x ', text)
        text = re.sub(r' (([buha]{3,} )|[buha]{3,}$)', r' _x ', text)
        text = re.sub(r'( (([ha]{2,} )|[ha]{2,}$)|(^[ha]{2,} ))', r' _x ', text)

        # hash tags
        # text = re.sub(r'#\w+', r' _h ', text)

        # good (happy) tags
        text = re.sub(r'[❤️😍😁🎉😀🤗🙂💪✌👍]+', r' _g ', text)
        text = re.sub(r'[8x:;]-?[\)\]\>]+', r' _g ', text)
        text = re.sub(r'[:;]-?[dp]+', r' _g ', text)
        # sad tags
        text = re.sub(r'[8x:;]-?[\(\[\<]+', r' _s ', text)
        text = re.sub(r'[🤮]+', r' _s ', text)
        text = re.sub(r'[😱🤦]+', r' _s ', text)
        # mad tags
        text = re.sub(r'[😡😠]+', r' _b ', text)

        # numbers
        text = re.sub(r'\d+', r' _n ', text)

        # remove rest non words symbols
        text = re.sub(r'[\W]+', r' ', text)
        text = re.sub(r'_+(( +)|($))', r' ', text)  # underline is part of 'word'

        # remove multi spaces
        text = re.sub(r'  +', r' ', text)

        tokens = text.split()
        tokens = [tk for tk in tokens if len(tk) > 0]

        # self.logger.debug(f"Output tokens: {tokens}")
        return tokens

    @staticmethod
    def remove_polish_letters(text):
        """Function will replace polish letters in text"""
        letters = {'ą': 'a', 'ć': 'c', 'ę': 'e', 'ó': 'o', 'ł': 'l',
                   'ń': 'n', 'ś': 's', 'ż': 'z', 'ź': 'z'}

        for pl, normal in letters.items():
            text = text.replace(pl, normal)

        return text

    # def normalize_text(self, text):
    #     """
    #     Remove stop words, and symbols. Remove every word shorter than min_word_len
    #     Args:
    #         text: string input
    #
    #     Returns:
    #
    #     """
    #     stop_words = get_stop_words(self.lang)  # default polish
    #     banned_symbols = [':', '"', "'", '.', '`', '”', '„', '/']
    #     banned_prefix = ['http']
    #
    #     text = text.lower()
    #     text = [word for word in text for pref in banned_prefix if
    #             not word.startswith(pref) and word not in banned_symbols and word not in stop_words]
    #
    #     return text

    def stemming(self, tokens):
        """
        Removes common prefixes and sufixes
        Args:
            list_array:

        Returns:

        """
        if self.lang == 'english' or self.lang is None:
            stemmer = LancasterStemmer()
            tokens = [stemmer.stem(word) for word in tokens]
        elif self.lang == 'polish':
            common_sufixes = ['bym',
                              'lam', 'lem', 'le', 'lo', 'li', 'iel', 'al',
                              'ja', 'yjna', 'yjnym',
                              'uja', 'uje', 'uje', 'uja', 'imi',
                              'ecie', 'anej', 'ej', 'eria',
                              'iemy', 'iesz', 'emy', 'em', 'ie', 'ia', 'eni',
                              'kow', 'ko', 'ka', 'ke', 'ek', 'kim',
                              'ac', 'amy', 'any', 'anie', 'a',
                              'acych', 'e',
                              'aj', 'ilem', 'u', 'ach', 'ch', 'om',
                              'ego',
                              'o', 'owi', 'owani', 'owy', 'owemu', 'owac', 'owym', 'owe', 'owie', 'ow',
                              'owny', 'ownosc',
                              'ym', 'emu',
                              'es', 'as',
                              'cie', 'ci', 'c',
                              'czne', 'czny', 'czna', 'cznie', 'czni',
                              'ami', 'ach', 'mi', 'im', 'in', 'i', 'y', 'uj']
            common_sufixes.sort(key=lambda x: -len(x))
            temp = tokens
            tokens = []
            for word in temp:
                if len(word) == 2:
                    tokens.append(word)
                else:
                    for sufix in common_sufixes:
                        if word.endswith(sufix):
                            word = word[:-len(sufix)]
                    if len(word) > 0:
                        tokens.append(word)
        return tokens

    def lematizing(self, list_array: 'list of pair <index, text>'):
        """
        Lematizing tokens to basic form
        Args:
            list_array:

        Returns:

        """
        pass


class Analyzer:
    def __init__(self, file_path, model_name,
                 passes=10, iterations=1000, topics=2, no_below=2, no_above=0.5,
                 lang='polish'):
        """Search and load processed .npy file first, if not found, open csv and do processing"""
        self.file_name = os.path.basename(file_path)
        self.model_name = model_name
        self.file_path = file_path
        self.model_dir = 'models'

        self.textprocessor = TextProcessor(lang=lang)
        self.logger = mini_logger('analyzer')

        self.passes = passes
        self.iterations = iterations
        self.topics = topics
        self.no_below = no_below
        self.no_above = no_above

        os.makedirs(self.model_dir, exist_ok=True)
        os.makedirs(os.path.join(self.model_dir, self.model_name), exist_ok=True)

        data = self.load_data()
        lda = self.load_model()

        if data is not None:
            self.data = data
        else:
            data = self.load_raw_data(file_path, ignore_rt=True)
            self.data = self.textprocessor.full_preprocess(data)
        #
        # self.all_words, self.count = self.get_all_words()
        #
        if lda is None:
            self.lda = None
            self.create_new_LDA_movel()
        else:
            self.lda = lda

    @staticmethod
    def load_raw_data(absolute_file_path, ignore_rt=True):
        """
        Loads raw csv with tweets
        CSV header, delimiter=';'
        user_id; screen_name; tweet_id; full_text
        Args:
            absolute_file_path:
        Returns:
        list:
            pair:
                <index, text>
        """
        with open(absolute_file_path, 'rt') as file:
            reader = csv.reader(file, delimiter=',')
            data = []
            for index, row in enumerate(reader):
                text = str(row[-1])
                if index == 0:
                    header = text
                    continue

                if ignore_rt and text.startswith('RT'):
                    continue
                else:
                    data.append((row[2], text))

            data = np.array(data)
            return data

    def create_new_LDA_movel(self):
        print("Creating LDA model")
        words = self.data[:, 1]
        dict = gensim.corpora.Dictionary(words)
        dict.filter_extremes(no_below=self.no_below, no_above=self.no_above)  # minimum 2 occuraces and no more than 20%
        print(dict)

        bow = [dict.doc2bow(text) for text in words]
        self.bow = bow

        lda = gensim.models.LdaMulticore(bow, num_topics=self.topics, id2word=dict,
                                         passes=self.passes, iterations=self.iterations)
        self.lda = lda

    def save_model(self):
        file_name = self.model_name
        full_path = os.path.join(self.model_dir, file_name)
        self.lda.save(full_path)

        print(f"Saved model: {file_name}")

    def load_model(self):
        file_name = self.model_name
        try:
            full_path = os.path.join(self.model_name, file_name)
            lda = gensim.models.LdaMulticore.load(full_path)
            print("Loaded model")
            return lda
        except FileNotFoundError:
            print(f"Not found this model: {file_name}")
            return None

    def load_data(self, file_name=None):
        if file_name is None:
            file_name = self.file_name
        try:
            data = np.load(os.path.join(self.model_name, file_name + '.npy'), allow_pickle=True)
            print(f"Loaded work data: {file_name}")
            return data
        except FileNotFoundError:
            print(f"Not found work data: {file_name}")
            return None

    def save_data(self, file_name=None):
        if file_name is None:
            file_name = self.file_name
        if self.data is not None:
            np.save(os.path.join(self.model_dir, file_name), self.data)
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

    def print_topics(self, n=-1):
        for x in range(self.topics):
            if n < 1:
                topics = self.lda.print_topic(x)
            else:
                topics = self.lda.print_topic(x, n)
            print(topics)

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

    all_files = glob.glob(os.path.join(directory, '*.csv'), recursive=True)
    file = all_files[-1]
    print(f"Selected file: {file}")

    topics = 2
    app = Analyzer(file_path=all_files[-1], model_name='tp-3', passes=50, iterations=1000, topics=topics,
                   no_below=15, no_above=0.7)
    app.print_topics()
    # app.create_new_LDA_movel()
    #

    #
    # for x in range(10):
    #     tweet = app.bow[x]
    #
    #     topics = app.lda[tweet]
    #     print(topics, tweet)
    #
    # app.save_data()
    # app.save_model()

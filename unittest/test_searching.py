from twitter_analyzer.analyzer.analyzer import Analyzer
import os
file_auto = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tweets', 'unittest_auto.csv'))
file_home = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tweets', 'unittest_home.csv'))
file_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tweets', 'unittest_parent.csv'))

words = 'text.1'


def test_search_in_files_1():
    app = Analyzer(auto_login=False)
    app.load_df([file_auto])
    app.filter_df_search_phrases(words, only_in_text=True)


def test_search_in_files_2():
    app = Analyzer(auto_login=False)
    app.load_df([file_home])
    app.filter_df_search_phrases(words, only_in_text=True)


def test_search_in_files_3():
    app = Analyzer(auto_login=False)
    app.load_df([file_parent])
    app.filter_df_search_phrases(words, only_in_text=True)


def test_search_in_files_4():
    app = Analyzer(auto_login=False)
    app.load_df([file_auto])
    app.filter_df_search_phrases(words, only_in_text=False)


def test_search_in_files_5():
    app = Analyzer(auto_login=False)
    app.load_df([file_home])
    app.filter_df_search_phrases(words, only_in_text=False)


def test_search_in_files_6():
    app = Analyzer(auto_login=False)
    app.load_df([file_parent])
    app.filter_df_search_phrases(words, only_in_text=False)

from twitter_analyzer.analyzer.tweet_operator import TwitterOperator
import os

file_auto = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tweets', 'unittest_auto.csv'))
file_home = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tweets', 'unittest_home.csv'))
file_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tweets', 'unittest_parent.csv'))

words = 'text.1'


def test_search_in_files_1():
    app = TwitterOperator(auto_login=False)
    app.load_df([file_auto])
    app.filter_df_search_phrases(words, only_in_text=True)


def test_search_in_files_2():
    app = TwitterOperator(auto_login=False)
    app.load_df([file_home])
    app.filter_df_search_phrases(words, only_in_text=True)


def test_search_in_files_3():
    app = TwitterOperator(auto_login=False)
    app.load_df([file_parent])
    app.filter_df_search_phrases(words, only_in_text=True)


def test_search_in_files_4():
    app = TwitterOperator(auto_login=False)
    app.load_df([file_auto])
    app.filter_df_search_phrases(words, only_in_text=False)


def test_search_in_files_5():
    app = TwitterOperator(auto_login=False)
    app.load_df([file_home])
    app.filter_df_search_phrases(words, only_in_text=False)


def test_search_in_files_6():
    app = TwitterOperator(auto_login=False)
    app.load_df([file_parent])
    app.filter_df_search_phrases(words, only_in_text=False)


words_2 = ''


def test_search_empty_files_1():
    app = TwitterOperator(auto_login=False)
    app.load_df([file_auto])
    app.filter_df_search_phrases(words_2, only_in_text=True)


def test_search_empty_files_2():
    app = TwitterOperator(auto_login=False)
    app.load_df([file_home])
    app.filter_df_search_phrases(words_2, only_in_text=True)


def test_search_empty_files_3():
    app = TwitterOperator(auto_login=False)
    app.load_df([file_parent])
    app.filter_df_search_phrases(words_2, only_in_text=True)


def test_search_empty_files_4():
    app = TwitterOperator(auto_login=False)
    app.load_df([file_auto])
    app.filter_df_search_phrases(words_2, only_in_text=False)


def test_search_empty_files_5():
    app = TwitterOperator(auto_login=False)
    app.load_df([file_home])
    app.filter_df_search_phrases(words_2, only_in_text=False)


def test_search_empty_files_6():
    app = TwitterOperator(auto_login=False)
    app.load_df([file_parent])
    app.filter_df_search_phrases(words_2, only_in_text=False)

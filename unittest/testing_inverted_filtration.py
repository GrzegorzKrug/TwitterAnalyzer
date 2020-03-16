from twitter_analyzer.analyzer.analyzer import Analyzer
import os
file_auto = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tweets', 'unittest_auto.csv'))
file_home = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tweets', 'unittest_home.csv'))
file_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tweets', 'unittest_parent.csv'))

words = "possibly_sensitive"


def test_1():
    app = Analyzer(auto_login=False)
    app.load_df([file_home])
    app.filter_by_existing_key(words, inverted=False)


def test_2():
    app = Analyzer(auto_login=False)
    app.load_df([file_home])
    app.filter_by_existing_key(words, inverted=False)


words = 'en'


def test_3():
    app = Analyzer(auto_login=False)
    app.load_df([file_home])
    app.filter_df_by_lang(words, inverted=False)


def test_4():
    app = Analyzer(auto_login=False)
    app.load_df([file_home])
    app.filter_df_by_lang(words, inverted=False)


words = "text"


def test_5a():
    app = Analyzer(auto_login=False)
    app.load_df([file_home])
    app.filter_df_search_phrases(words, only_in_text=True, inverted=False)


def test_5b():
    app = Analyzer(auto_login=False)
    app.load_df([file_home])
    app.filter_df_search_phrases(words, only_in_text=False, inverted=False)


def test_6a():
    app = Analyzer(auto_login=False)
    app.load_df([file_home])
    app.filter_df_search_phrases(words, only_in_text=True, inverted=True)


def test_6b():
    app = Analyzer(auto_login=False)
    app.load_df([file_home])
    app.filter_df_search_phrases(words, only_in_text=False, inverted=True)


current_id = '1236785069022416902'


def test_7():
    app = Analyzer(auto_login=False)
    app.load_df([file_home])
    app.filter_df_by_tweet_id(current_id, inverted=False)


def test_8():
    app = Analyzer(auto_login=False)
    app.load_df([file_home])
    app.filter_df_by_tweet_id(current_id, inverted=True)


user_id = '1194893840'


# def test_9():
#     app = Analyzer(auto_login=False)
#     app.load_df([file_home])
#     app.filter_df_by_user(user_id, inverted=False)
#
#
# def test_10():
#     app = Analyzer(auto_login=False)
#     app.load_df([file_home])
#     app.filter_df_by_user(user_id, inverted=True)

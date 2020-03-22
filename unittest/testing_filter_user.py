from twitter_analyzer.analyzer.tweet_operator import TwitterOperator
import os

file_auto = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tweets', 'unittest_auto.csv'))
file_home = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tweets', 'unittest_home.csv'))
file_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tweets', 'unittest_parent.csv'))

words = 'adam'


def test_filter_df_by_user_in_files_1():
    app = TwitterOperator()
    app.load_df([file_auto])
    app.filter_df_by_user(words)


def test_filter_df_by_user_in_files_2():
    app = TwitterOperator()
    app.load_df([file_home])
    app.filter_df_by_user(words)


def test_filter_df_by_user_in_files_3():
    app = TwitterOperator()
    app.load_df([file_parent])
    app.filter_df_by_user(words)


def test_filter_df_by_user_in_files_4():
    app = TwitterOperator()
    app.load_df([file_auto])
    app.filter_df_by_user(words)


def test_filter_df_by_user_in_files_5():
    app = TwitterOperator()
    app.load_df([file_home])
    app.filter_df_by_user(words)


def test_filter_df_by_user_in_files_6():
    app = TwitterOperator()
    app.load_df([file_parent])
    app.filter_df_by_user(words)


words_2 = ''


def test_filter_df_by_user_empty_files_1():
    app = TwitterOperator()
    app.load_df([file_auto])
    app.filter_df_by_user(words_2)


def test_filter_df_by_user_empty_files_2():
    app = TwitterOperator()
    app.load_df([file_home])
    app.filter_df_by_user(words_2)


def test_filter_df_by_user_empty_files_3():
    app = TwitterOperator()
    app.load_df([file_parent])
    app.filter_df_by_user(words_2)


def test_filter_df_by_user_empty_files_4():
    app = TwitterOperator()
    app.load_df([file_auto])
    app.filter_df_by_user(words_2)


def test_filter_df_by_user_empty_files_5():
    app = TwitterOperator()
    app.load_df([file_home])
    app.filter_df_by_user(words_2)


def test_filter_df_by_user_empty_files_6():
    app = TwitterOperator()
    app.load_df([file_parent])
    app.filter_df_by_user(words_2)


words_3 = "120850825"


def test_filter_df_by_user_id_files_1():
    app = TwitterOperator()
    app.load_df([file_auto])
    app.filter_df_by_user(words_3)


def test_filter_df_by_user_id_files_2():
    app = TwitterOperator()
    app.load_df([file_home])
    app.filter_df_by_user(words_3)


def test_filter_df_by_user_id_files_3():
    app = TwitterOperator()
    app.load_df([file_parent])
    app.filter_df_by_user(words_3)


def test_filter_df_by_user_id_files_4():
    app = TwitterOperator()
    app.load_df([file_auto])
    app.filter_df_by_user(words_3)


def test_filter_df_by_user_id_files_5():
    app = TwitterOperator()
    app.load_df([file_home])
    app.filter_df_by_user(words_3)


def test_filter_df_by_user_id_files_6():
    app = TwitterOperator()
    app.load_df([file_parent])
    app.filter_df_by_user(words_3)

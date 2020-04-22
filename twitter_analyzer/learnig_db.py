from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError, IntegrityError

import time
from analyzer.database_operator import Tweet, User
from analyzer.database_operator import add_tweet_with_user


def get_engine():
    dbname = 'postgres'
    user = 'admin'
    password = 'docker'

    host = '127.0.0.1'
    port = 5432
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    # url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

    engine = create_engine(url,
                           connect_args={'client_encoding': 'utf8'})
    return engine


Base = declarative_base()
engine = get_engine()
Session = sessionmaker(bind=engine)


def show_tables():
    tables = engine.table_names()
    print(f"Tables: {tables}")


def show_tweets():
    session = Session()
    # for r in session.query(Tweet).filter(Tweet.tweet_id == 1245478587177865219):
    for r in session.query(Tweet).all():
        print(r)


def show_users():
    session = Session()
    for r in session.query(User).all():
        print(r)


def show_db_size():
    session = Session()
    tweet_count = session.query(Tweet).count()
    user_count = session.query(User).count()
    print(f"Tweets: {tweet_count}, Users: {user_count}")


show_tables()
show_db_size()

sess = Session()

tweets = sess.query(Tweet.tweet_id).all()
first = tweets[0][0]
print(first)

find_tweet = sess.query(Tweet.full_text).filter(Tweet.tweet_id == first).all()
print(find_tweet)

first_author = sess.query(User.user_id).first()
author_tweets = sess.query(Tweet.full_text, Tweet.tweet_id).filter(Tweet.user_id == first_author).all()
print(author_tweets)

look_for = 1587569773
first_timestmp = sess.query(Tweet.tweet_id, Tweet.full_text).filter(Tweet.created_at == look_for).all()
print(first_timestmp)

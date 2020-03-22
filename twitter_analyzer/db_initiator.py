from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from psycopg2 import OperationalError

import time
import psycopg2
import os

Base = declarative_base()


class Tweet(Base):
    __tablename__ = 'tweet'
    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer)
    contributors = Column(String)
    coordinates = Column(String)
    created_at = Column(String)
    current_user_retweet = Column(Integer)
    favorite_count = Column(Integer)
    favorited = Column(String)
    full_text = Column(String)
    geo = Column(String)
    hashtags = Column(String)
    in_reply_to_screen_name = Column(String)
    in_reply_to_status_id = Column(Integer)
    in_reply_to_user_id = Column(Integer, ForeignKey('user.id'))
    lang = Column(String)
    location = Column(String)
    media = Column(String)
    place = Column(String)
    possibly_sensitive = Column(String)
    quoted_status = Column(String)
    quoted_status_id = Column(Integer)
    retweet_count = Column(Integer)
    retweeted = Column(String)
    retweeted_status = Column(String)
    scopes = Column(String)
    source = Column(String)
    truncated = Column(String)
    urls = Column(String)
    user = Column(Integer, ForeignKey('user.id'))
    user_mentions = Column(String)
    withheld_copyright = Column(String)
    withheld_in_countries = Column(String)
    withheld_scope = Column(String)
    tweet_mode = Column(String)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    alias = Column(String)


def setup_engine():
    dbname = 'postgres'
    user = 'admin'
    password = 'docker'
    host = os.getenv('DB_ACCES_NAME', '127.0.0.1')
    port = 5432
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    engine = create_engine(url,
                           connect_args={'client_encoding': 'utf8'})
    return engine


def initiate():
    engine = setup_engine()
    Base.metadata.create_all(engine)
    print("DB initiation finished")


if __name__ == '__main__':
    print("Initializing DB")
    while True:
        try:
            initiate()
            print("Initiation successfully!")
            break
        except Exception as e:
            print(f"Waiting for DB.")
            time.sleep(5)

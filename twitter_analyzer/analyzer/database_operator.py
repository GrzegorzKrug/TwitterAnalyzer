from sqlalchemy import Column, Integer, String, ForeignKey, Table, BigInteger
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import ProgrammingError, IntegrityError
from sqlalchemy.orm import sessionmaker
from psycopg2 import OperationalError
from .custom_logger import define_logger

import time
import os
import sys

Base = declarative_base()
logger = define_logger("DB_Orm")


class Tweet(Base):
    __tablename__ = 'tweet'
    tweet_id = Column(String, primary_key=True)
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
    in_reply_to_status_id = Column(String)
    in_reply_to_user_id = Column(String)
    lang = Column(String)
    location = Column(String)
    media = Column(String)
    place = Column(String)
    possibly_sensitive = Column(String)
    quoted_status_id = Column(String)
    retweet_count = Column(Integer)
    retweeted = Column(String)
    retweeted_status_id = Column(String)
    scopes = Column(String)
    source = Column(String)
    truncated = Column(String)
    urls = Column(String)
    user_id = Column(BigInteger)
    user_mentions = Column(String)
    withheld_copyright = Column(String)
    withheld_in_countries = Column(String)
    withheld_scope = Column(String)
    tweet_mode = Column(String)

    def __repr__(self):
        return f"{self.tweet_id}: ".ljust(20) + f"{self.full_text}"


class User(Base):
    __tablename__ = "user"
    id = Column(String, primary_key=True)
    name = Column(String)
    alias = Column(String)


def get_engine():
    dbname = 'postgres'
    user = 'admin'
    password = 'docker'
    host = os.getenv('DB_ACCES_NAME', '127.0.0.1')
    port = 5432
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    engine = create_engine(url,
                           connect_args={'client_encoding': 'utf8'})
    return engine


def initialize():
    logger.debug("Initializing DB")
    t_start = time.time()
    while True:
        try:
            engine = get_engine()
            Base.metadata.create_all(engine)
            logger.debug("DB Initialization finished!")
            break
        except Exception as e:
            logger.warning(e)
            if time.time() - t_start > 60:
                logger.error("Task timeout: 60 sec.")
                sys.exit(1)
            logger.debug(f"Waiting for DB.")
            time.sleep(5)


def add_tweet(
        Session,
        # Tweet required
        tweet_id,
        timestamp,
        full_text,
        created_at,

        # User required
        user_id,
        user_name,

        # Tweet optional
        contributors=None,
        coordinates=None,
        current_user_retweet=None,
        favorite_count=None,
        favorited=None,
        geo=None,
        hashtags=None,
        in_reply_to_status_id=None,
        in_reply_to_user_id=None,
        lang=None,
        location=None,
        media=None,
        place=None,
        possibly_sensitive=None,
        quoted_status_id=None,
        retweet_count=None,
        retweeted=None,
        retweeted_status_id=None,
        scopes=None,
        source=None,
        truncated=None,
        urls=None,
        user_mentions=None,
        withheld_copyright=None,
        withheld_in_countries=None,
        withheld_scope=None,
        tweet_mode=None,

        # User Optional
        user_alias=None
):

    tweet = Tweet(tweet_id=str(tweet_id),
                  timestamp=timestamp,
                  contributors=contributors,
                  coordinates=coordinates,
                  created_at=created_at,
                  current_user_retweet=current_user_retweet,
                  favorite_count=favorite_count,
                  favorited=favorited,
                  full_text=full_text,
                  geo=geo,
                  hashtags=hashtags,
                  in_reply_to_status_id=str(in_reply_to_status_id),
                  in_reply_to_user_id=str(in_reply_to_user_id),
                  lang=lang,
                  location=location,
                  media=media,
                  place=place,
                  possibly_sensitive=possibly_sensitive,
                  quoted_status_id=str(quoted_status_id),
                  retweet_count=retweet_count,
                  retweeted=retweeted,
                  retweeted_status_id=str(retweeted_status_id),
                  scopes=scopes,
                  source=source,
                  truncated=truncated,
                  urls=urls,
                  user_id=str(user_id),
                  user_mentions=user_mentions,
                  withheld_copyright=withheld_copyright,
                  withheld_in_countries=withheld_in_countries,
                  withheld_scope=withheld_scope,
                  tweet_mode=tweet_mode)

    user = User(id=user_id, name=user_name, alias=user_alias)
    session = Session()
    try:
        insert_to_table(session, tweet)
        logger.debug(f'Inserting to table. tweet_id: {tweet_id}, timestamp: {timestamp}')
    except IntegrityError:
        logger.warning(f"Possible tweet duplicate: {tweet_id}")
        session.rollback()
        pass

    session = Session()
    try:
        insert_to_table(session, user)
        logger.debug(f'Inserted to table. user_id: {user_id}, timestamp: {timestamp}')
    except IntegrityError:
        logger.warning(f"Possible user duplicate: {user_id}")


def get_database_connectors() -> "Engine, Session":
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return engine, Session


def insert_to_table(session, table_object):
    try:
        session.add(table_object)
        session.commit()
    except OperationalError as e:
        logger.error(f"OperationalError: {e}")

    except ProgrammingError as pe:
        logger.error(f"ProgrammingError: {pe}")


# if __name__ == '__main__':
#     initialize()

from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean, BigInteger
from sqlalchemy.exc import ProgrammingError, IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from .custom_logger import define_logger
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine

import time
import sys
import os
import re

Base = declarative_base()
logger = define_logger("DB_Orm")


class User(Base):
    __tablename__ = "user"
    user_id = Column(BigInteger, primary_key=True)
    user_name = Column(String)
    screen_name = Column(String)
    user_location = Column(String)
    description = Column(String)
    user_url = Column(String)
    followers_count = Column(String)
    friends_count = Column(String)
    listed_count = Column(String)
    created_at = Column(BigInteger)
    verified = Column(Boolean)
    statuses_count = Column(String)
    user_lang = Column(String)
    timestamp = Column(BigInteger)

    def __repr__(self):
        return f"User: {self.user_id}: {self.screen_name} as {self.user_name}"


class Tweet(Base):
    __tablename__ = 'tweet'
    tweet_id = Column(BigInteger, primary_key=True)
    timestamp = Column(BigInteger)
    contributors = Column(String)
    coordinates = Column(String)
    created_at = Column(BigInteger)
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
    source_status_id = Column(String)
    truncated = Column(String)
    urls = Column(String)
    user_id = Column(BigInteger, ForeignKey('user.user_id'))
    user_mentions = Column(String)
    withheld_copyright = Column(String)
    withheld_in_countries = Column(String)
    withheld_scope = Column(String)
    tweet_mode = Column(String)

    def __repr__(self):
        return f"{self.tweet_id}: ".ljust(20) + f"{self.full_text}"


# class TweetWork(Tweet):  # not working
#     Tweet.__tablename__ = "tweet_work"
#     Tweet.__tablename__ = "tweet_work"
#
#
# class UserWork(User):  # not working
#     User.__tablename__ = "user_work"


def get_engine():
    dbname = 'postgres'
    user = 'admin'
    password = 'docker'
    host = os.getenv('DB_ACCES_NAME', '127.0.0.1')
    port = 5432
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    engine = create_engine(url, pool_size=250,
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


def add_tweet_with_user(
        Session,
        timestamp,

        # Tweet required
        tweet_id,
        full_text,
        created_at,

        # User required
        user_id,
        user_name,
        screen_name,
        #
        overwrite=False,

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
        source_status_id=None,
        truncated=None,
        urls=None,
        user_mentions=None,
        withheld_copyright=None,
        withheld_in_countries=None,
        withheld_scope=None,
        tweet_mode=None,

        # User Optional
        user_location=None,
        description=None,
        user_url=None,
        followers_count=None,
        friends_count=None,
        listed_count=None,
        user_created_at=None,
        verified=None,
        statuses_count=None,
        user_lang=None
):
    add_user(
            Session=Session,
            user_id=user_id,
            user_name=user_name,
            screen_name=screen_name,
            user_location=user_location,
            description=description,
            user_url=user_url,
            followers_count=followers_count,
            friends_count=friends_count,
            listed_count=listed_count,
            created_at=user_created_at,
            verified=verified,
            statuses_count=statuses_count,
            user_lang=user_lang,
            timestamp=timestamp,
            overwrite=overwrite
    )

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
                  source_status_id=source_status_id,
                  truncated=truncated,
                  urls=urls,
                  user_id=str(user_id),
                  user_mentions=user_mentions,
                  withheld_copyright=withheld_copyright,
                  withheld_in_countries=withheld_in_countries,
                  withheld_scope=withheld_scope,
                  tweet_mode=tweet_mode,
                  )

    session = Session()
    if overwrite:
        tw = session.query(Tweet).filter(Tweet.tweet_id == tweet_id).first()
        if tw:
            logger.debug(f"Deleting tweet: {tweet_id}")
            session.delete(tw)
            session.flush()
    try:
        insert_to_table(session, tweet)
        logger.debug(f'Inserting tweet to table, id: {tweet_id}, timestamp: {timestamp}')
    except IntegrityError:
        logger.warning(f"Possible tweet duplicate: {tweet_id}")
        session.rollback()
        pass
    session.close()


def add_user(
        Session,
        user_id,
        user_name,
        screen_name,
        user_location,
        description,
        user_url,
        followers_count,
        friends_count,
        listed_count,
        created_at,
        verified,
        statuses_count,
        user_lang,
        timestamp,
        overwrite=False
):
    session = Session()
    user = User(
            user_id=user_id,
            user_name=user_name,
            screen_name=screen_name,
            user_location=user_location,
            description=description,
            user_url=user_url,
            followers_count=followers_count,
            friends_count=friends_count,
            listed_count=listed_count,
            created_at=created_at,
            verified=verified,
            statuses_count=statuses_count,
            user_lang=user_lang,
            timestamp=timestamp
    )
    # if overwrite:
    #     tw = session.query(User).filter(User.user_id == user_id).first()
    #     if tw:
    #         logger.debug(f"Deleting user: {screen_name}")
    #         session.delete(tw)
    #         session.flush()
    try:
        insert_to_table(session, user)
        logger.debug(f'Inserted user to table. screen_name: {screen_name:>20}, '
                     f'user_id: {user_id}, timestamp: {timestamp}')
    except IntegrityError:
        logger.warning(f"User in table: {user_id}, {screen_name}")
    session.close()


def get_database_connectors() -> "Engine, Session":
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return engine, Session


def insert_to_table(session, table_object):
    try:
        session.add(table_object)
        session.commit()
    except OperationalError as e:
        logger.error(f"OperationalError when inserting to table: '{e}'")
    except ProgrammingError as pe:
        logger.error(f"ProgrammingError when inserting to table.")


def filter_by_lang(Session, lang, inverted=False):
    """

    Args:
        lang: language to filter
        inverted:

    Returns:

    """
    lang = str(lang)
    session = Session()
    if not inverted:
        tweets = session.query(Tweet.tweet_id, Tweet.lang).filter(Tweet.lang == lang).all()
    else:
        tweets = session.query(Tweet.tweet_id, Tweet.lang).filter(Tweet.lang != lang).all()
    session.close()
    return tweets


# def filter_by_existing_key(Session, key, inverted=False):
#     """
#     Filter db, to get all tweets with key
#     Args:
#         key: string
#         inverted: bool, inverted filtraion
#
#     Returns:
#
#     """
#     session = Session()
#     if not inverted:
#         text = f"session.query(Tweet.tweet_id, Tweet.{key}).filter(Tweet.{key} != 'None').all()"
#     else:
#         text = f"session.query(Tweet.tweet_id, Tweet.{key}).filter(Tweet.{key} == 'None').all()"
#     tweets = eval(text)
#     return tweets


def filter_db_search_words(Session, input_string):
    """

    Args:
        Session:
        words:

    Returns:

    """
    # stages = re.split(';', words)  # Separating stages
    input_string = input_string.lower()
    stages = re.split(r"[;]", input_string)

    for stage_ind, stage in enumerate(stages):
        words = re.split(r"[,. !@#$%^&*]", stage)
        for i, word in enumerate(words):
            word = ''.join(letter for letter in word if letter not in "!?,. ;'\\\"()!@#$%^&*()_)+_-[]")
            word = word.lstrip(" ").rstrip(" ")
            words[i] = word
        words = [word for word in words if len(word) > 0]
        stages[stage_ind] = words
    stages = [stage for stage in stages if len(stage) > 0]

    session = Session()

    tweets = []
    logger.debug(f"Searching tweets, staged: {stages}")

    words = stages[0]
    for word in words:
        output = [tweet for tweet in session.query(Tweet.tweet_id, Tweet.full_text).all() if
                  word.lower() in tweet[1].lower()]
        tweets += output

    tweets = set(tweets)  # drop duplicates
    for run_ind in range(1, len(stages)):
        stage = stages[run_ind]
        old_tweets = tweets.copy()
        tweets = []
        for tweet in old_tweets:
            for word in stage:
                if word in tweet[1].lower():
                    tweets.append(tweet)
                    break

    session.close()
    return tweets


def filter_db_search_phrases(Session, words):
    """

    Args:
        Session:
        words:

    Returns:

    """
    stages = re.split(r'[,.!;?]', words)  # Separating stages
    for i, word in enumerate(stages):
        word = ''.join(letter for letter in word if letter not in "'\\\"()@#$%^&*()_)+_-[]")
        word = word.lstrip(" ").rstrip(" ")
        stages[i] = word
    phrases = [phrases for phrases in stages if len(phrases) > 0]

    session = Session()
    tweets = []
    logger.debug(f"Searching tweets, phrases: {phrases}")
    for phrase in phrases:
        output = [tweet for tweet in session.query(Tweet.tweet_id, Tweet.full_text).all() if
                  phrase.lower() in tweet[1].lower()]
        tweets += output
    session.close()
    return tweets


def get_db_full_tweet_with_user(Session, tweet_id):
    session = Session()
    tweet_id = int(tweet_id)
    tweet = session.query(Tweet, User).join(User).filter(Tweet.tweet_id == tweet_id).first()
    session.close()
    return tweet


def get_db_all_tweet_list(Session):
    session = Session()
    tweets = session.query(Tweet.tweet_id).all()
    session.close()
    return tweets


def drop_existing_tweets(Session, tweet_id_list):
    session = Session()
    tweets = [tw_id for tw_id in tweet_id_list if not session.query(Tweet).filter(Tweet.tweet_id == tw_id).first()]
    session.close()
    return tweets

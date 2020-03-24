from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError, IntegrityError

import time
from analyzer.database_operator import Tweet, User
from analyzer.database_operator import add_tweet


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
    print(f"Tables after drop: {tables}")


def show_tweets():
    session = Session()
    for r in session.query(Tweet).all():
        print(r)


show_tables()
show_tweets()
#
# add_tweet(Session(), 152, full_text="Witam w sklepie.", timestamp=15,
#           created_at="dzisiaj", user_id=67, user_name="Pawel")

# show_tweets()
# show_users()

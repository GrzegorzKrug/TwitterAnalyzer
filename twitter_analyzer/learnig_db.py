from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import psycopg2
import time


Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    email = Column(String)

    def __repr__(self):
        return f"<User(name='{self.name}', address='{self.address}', email='{self.email}')>"


def setup_engine():
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


engine = setup_engine()
Session = sessionmaker(bind=engine)


c1 = Customer(name='Ravi Kumar', email='ravi@gmail.com')
c2 = Customer(name='Ali baba', address='Station', email='ravi@gmail.com')
c3 = Customer(name='Ali baba', address='Station')
c4 = Customer(name='Ali baba', address='Pren House')


try:
    tables = engine.table_names()
    print(f"Tables in db: {tables}")

    # Base.metadata.create_all(engine)
    # tables = engine.table_names()
    # print(f"Current tables: {tables}")

    # session = Session()
    # session.add(c1)
    # session.add(c2)
    # session.commit()

    # with engine.connect() as connection:
    #     tables = engine.table_names()
    #     for table in tables:
    #         # if table != 'customers':
    #         #     continue
    #         connection.execute(f"DROP TABLE {table}")
    #         print(f"Dropping table: {table}")

    # session = Session()
    # result = session.query(Customer).all()
    # for row in result:
    #     print(row)

except psycopg2.OperationalError as e:
    print(f"Exception: {e}")

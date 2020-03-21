from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import time

Base = declarative_base()


def clear_tables():
    tables = engine.table_names()
    if tables:
        with engine.connect() as connection:
            for tab in tables:
                connection.execute(f"DROP TABLE {tab}")
                print(f"Dropped: {tab}")


class Customers(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    email = Column(String)


def setup_engine():
    dbname = 'postgres'
    user = 'admin'
    password = 'docker'

    host = '127.0.0.1'
    port = 5432
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

    engine = create_engine(url,
                           connect_args={'client_encoding': 'utf8'}
                       )
    return engine


engine = setup_engine()
clear_tables()
Base.metadata.create_all(engine)


from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

c1 = Customers(name='Ravi Kumar', email='ravi@gmail.com')
c2 = Customers(name='Ali baba', address='Station', email='ravi@gmail.com')
c3 = Customers(name='Ali baba', address='Station')
c4 = Customers(name='Ali baba', address='Pren House')

session.add(c1)
session.add(c2)
session.add(c4)
session.commit()

session = Session()
result = session.query(Customers).all()

for row in result:
    print("Name: ", row.name, "Address:", row.address, "Email:", row.email)
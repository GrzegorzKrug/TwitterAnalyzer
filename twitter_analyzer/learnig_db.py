from sqlalchemy import create_engine

dbname = 'postgres'
user = 'admin'
password = 'docker'

host = '127.0.0.1'
port = 5432
url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

engine = create_engine(url,
                       connect_args={'client_encoding': 'utf8'}
                       )


with engine.connect() as connection:
    pass
    # result = connection.execute("select username from users")
    # for row in result:
    #     print("username:", row['username'])
from sqlalchemy import create_engine

user = 'greg'
password = 123
host = 'host'
port = 5432
dbname = 'dbname'
url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

engine = create_engine(url)

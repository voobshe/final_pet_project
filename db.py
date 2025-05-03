from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from bot_key import DB_PASS

# #!!!!!!!!!!!!!!!!!!!!!!!!!!!! УБЕРИ КЛЮЧ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# engine = create_engine(
#     'postgresql://postgres:.....@lyrically-happy-rudd.data-1.use1.tembo.io:5432/postgres'
# )
# db_session = scoped_session(sessionmaker(bind=engine))

# class Base(DeclarativeBase):
#     pass

DB_USER = "postgres"
DB_HOST = "lyrically-happy-rudd.data-1.use1.tembo.io"
DB_PORT = "5432"
DB_NAME = "postgres"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHAMY_DATABASE_URL = 'mysql://admin:iMUAUlu3@mysql-68971-0.cloudclusters.net:10284/wallart_backend'

# SQLALCHAMY_DATABASE_URL = 'sqlite:///./products.db'

engine = create_engine(SQLALCHAMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

Base = declarative_base()

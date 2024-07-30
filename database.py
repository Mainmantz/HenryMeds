from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from databases import Database
from sqlalchemy.orm import Session

DATABASE_URL = "postgresql://localhost/henrydb"

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Dependency to get the database session
def get_session():
    with Session(engine) as session:
        yield session
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///BOOK.db")

# Create a DeclarativeMeta instance
Base = declarative_base()

# Define To Do class inheriting from Base
class Book(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    title =  Column(String(50))
    description =  Column(String(50))

# Create the database
Base.metadata.create_all(engine)
import uuid

from sqlalchemy import Column, Integer, String
from .Base import Base  # Assuming you are using Base from your Base.py file


class Questions(Base):
    __tablename__ = "questions"  # This will create a table named 'questions' in the DB

    id = Column(Integer, primary_key=True, index=True, default=uuid.uuid4)
    category = Column(String, index=True)
    value = Column(Integer)
    question = Column(String)
    answer = Column(String)

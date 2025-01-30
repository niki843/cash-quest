import os
import uuid

from dotenv import load_dotenv
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


class Questions(Base):
    __tablename__ = "questions"

    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    category = Column(String, nullable=False)
    value = Column(Integer, nullable=False)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

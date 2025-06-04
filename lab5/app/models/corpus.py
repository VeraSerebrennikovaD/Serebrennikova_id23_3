from sqlalchemy import Column, Integer, String, Text
from app.db.base import Base

class Corpus(Base):
    __tablename__ = "corpuses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)

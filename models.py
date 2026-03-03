from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

class ChatHistory(Base):
    __tablename__ = "chathistory"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    query = Column(Text)
    response = Column(Text)
    
class LegalKnowledge(Base):
    __tablename__ = "legal_knowledge"

    id = Column(Integer, primary_key=True, index=True)
    section = Column(String, index=True)
    title = Column(String)
    description = Column(Text)

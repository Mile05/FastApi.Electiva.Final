from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    password = Column(String)
    full_name = Column(String)

class UserBase(BaseModel):
    username: str
    full_name: str
    
class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    
class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from .base import Base

from sqlalchemy.orm import relationship

# Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    products = relationship("Product", back_populates="category")

class CategoryResponse(BaseModel):
    id: int
    name: str

class CategoryCreate(BaseModel):
    name: str

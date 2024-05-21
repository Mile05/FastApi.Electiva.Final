from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from app.models.category import Category

from .base import Base

# Base = declarative_base()

class Product(Base):
    # from app.models.venta import Venta
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer)
    stock = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship(Category, back_populates="products")
    
    venta = relationship("Venta", back_populates="product")

class ProductCreate(BaseModel):
    name: str
    price: int
    stock: int
    category_id: int
    
class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    stock: int
    category_id: int

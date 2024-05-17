from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from app.models.product import Product
from sqlalchemy.ext.declarative import declarative_base
from .base import Base

# Base = declarative_base()

class Venta(Base):
    __tablename__ = "venta"

    id = Column(Integer, primary_key=True, index=True)
    id_product = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    observation = Column(String)
    
    product = relationship("Product", back_populates="venta")
    
class VentaCreate(BaseModel):
    id_product: int
    quantity: int
    observation: str
    
class VentaResponse(BaseModel):
    id: int
    id_product: str
    quantity: str
    observation: str

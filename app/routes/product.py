from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from db.mysql import SessionLocal, get_db
from app.models.product import Product, ProductCreate, ProductResponse
from helpers.httpBearer import get_current_user
from app.models.token import TokenData

router = APIRouter()

@router.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate, 
                   db: Session = Depends(get_db),
                   current_user: TokenData = Depends(get_current_user)):
    new_product = Product(name=product.name, price=product.price, stock=product.stock, category_id=product.category_id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, 
                 db: Session = Depends(get_db),
                 current_user: TokenData = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/products", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db),
                     current_user: TokenData = Depends(get_current_user)):
    products = db.query(Product).all()
    return products

@router.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, 
                   db: Session = Depends(get_db),
                   current_user: TokenData = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return
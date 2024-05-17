from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from db.mysql import SessionLocal, get_db
from app.models.category import Category, CategoryResponse, CategoryCreate

router = APIRouter()

@router.post("/categories/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    new_category = Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("/categories/{category_id}", response_model=CategoryResponse)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/categories/", response_model=List[CategoryResponse])
def get_all_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories

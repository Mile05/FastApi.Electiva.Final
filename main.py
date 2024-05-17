import os
from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "flask_db")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
# Replace 'your_username', 'your_password' and 'your_database' with your actual MySQL credentials
# SQLALCHEMY_DATABASE_URL = "mysql://your_username:your_password@localhost/your_database"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define SQLAlchemy models
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class CategoryResponse(BaseModel):
    id: int
    name: str

class CategoryCreate(BaseModel):
    name: str
    
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer)
    stock = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"))
    
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

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    password = Column(String)
    full_name = Column(String)

class Venta(Base):
    __tablename__ = "venta"

    id = Column(Integer, primary_key=True, index=True)
    id_product = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    observation = Column(String)
    
class UserBase(BaseModel):
    username: str
    full_name: str
    
class VentaResponse(BaseModel):
    id: int
    id_product: str
    quantity: str
    observation: str

class UserResponse(BaseModel):
    id: int
    password: str
    username: str
    full_name: str
    
class UserCreate(BaseModel):
    password: str
    username: str
    full_name: str

class VentaCreate(BaseModel):
    id_product: int
    quantity: int
    observation: str


app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD operations for categories
@app.post("/categories/")
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    new_category = Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@app.get("/categories/{category_id}")
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@app.get("/categories/", response_model=List[CategoryResponse])
def get_all_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return [{"id": category.id, "name": category.name} for category in categories]


@app.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(name=product.name, price=product.price, stock=product.stock, category_id=product.category_id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/products/{product_id}")
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/products/", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@app.post("/users/", response_model=None)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(full_name=user.full_name, username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get all users
@app.get("/users/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# Get a user by id
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Create a new venta
@app.post("/ventas/", response_model=None)
def create_venta(venta: VentaCreate, db: Session = Depends(get_db)):
    new_venta = Venta(id_product=venta.id_product, quantity=venta.quantity, observation=venta.observation)
    db.add(new_venta)
    db.commit()
    db.refresh(new_venta)
    return new_venta

# Get all ventas
@app.get("/ventas/", response_model=List[VentaResponse])
def get_all_ventas(db: Session = Depends(get_db)):
    ventas = db.query(Venta).all()
    return ventas

# Get a venta by id
@app.get("/ventas/{venta_id}", response_model=VentaResponse)
def get_venta(venta_id: int, db: Session = Depends(get_db)):
    venta = db.query(Venta).filter(Venta.id == venta_id).first()
    if venta is None:
        raise HTTPException(status_code=404, detail="Venta not found")
    return venta
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from db.mysql import SessionLocal, get_db
from app.models.venta import Venta, VentaCreate, VentaResponse

router = APIRouter()

@router.post("/ventas", response_model=VentaResponse)
def create_venta(venta: VentaCreate, db: Session = Depends(get_db)):
    new_venta = Venta(id_product=venta.id_product, quantity=venta.quantity, observation=venta.observation)
    db.add(new_venta)
    db.commit()
    db.refresh(new_venta)
    return new_venta

@router.get("/ventas/{venta_id}", response_model=VentaResponse)
def read_venta(venta_id: int, db: Session = Depends(get_db)):
    venta = db.query(Venta).filter(Venta.id == venta_id).first()
    if venta is None:
        raise HTTPException(status_code=404, detail="Venta not found")
    return venta

@router.get("/ventas", response_model=List[VentaResponse])
def get_all_ventas(db: Session = Depends(get_db)):
    ventas = db.query(Venta).all()
    return ventas

@router.delete("/ventas/{venta_id}", status_code=204)
def delete_product(venta_id: int, 
                   db: Session = Depends(get_db)):
    product = db.query(Venta).filter(Venta.id == venta_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Venta not found")
    
    db.delete(product)
    db.commit()
    return
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Payee)
def create_payee(payee: schemas.PayeeCreate, db: Session = Depends(get_db)):
    return crud.create_payee(db=db, payee=payee)

@router.get("/{user_id}", response_model=list[schemas.Payee])
def read_payees(user_id: int, db: Session = Depends(get_db)):
    return crud.get_payees(db, user_id=user_id)
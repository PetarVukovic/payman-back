from sqlalchemy.orm import Session
from . import models, schemas

# USERS CRUD

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# PAYEES CRUD

def create_payee(db: Session, payee: schemas.PayeeCreate):
    db_payee = models.Payee(**payee.model_dump())
    db.add(db_payee)
    db.commit()
    db.refresh(db_payee)
    return db_payee

def get_payees(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Payee).filter(models.Payee.user_id == user_id).offset(skip).limit(limit).all()

def get_payee(db: Session, payee_id: int):
    return db.query(models.Payee).filter(models.Payee.id == payee_id).first()
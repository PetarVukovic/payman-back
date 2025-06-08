from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.payman_service import PaymanService
from app import crud

router = APIRouter()

@router.post("/payman-sync/")
def payman_sync(question: str, user_email: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    response = PaymanService.ask_payman(question)
    PaymanService.log_payman_response(db, response, user_id=user.id)
    PaymanService.parse_and_store_response(response, db, user_id=user.id)
    return {"message": "Payees processed and stored successfully"}
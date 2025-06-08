from fastapi import FastAPI
from app.database import Base, engine
from app.api import payments, users, payees

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(payees.router, prefix="/payees", tags=["Payees"])
app.include_router(payments.router, prefix="/payments", tags=["Payments"])
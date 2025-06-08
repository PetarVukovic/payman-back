from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# USERS

class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    subscription_plan: Optional[str] = None

class UserCreate(UserBase):
    password_hash: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class ConfigDict:
        from_attributes = True

# PAYEES

class PayeeBase(BaseModel):
    supplier_name: str
    iban: str
    wallet_address: Optional[str]
    kyc_status: Optional[str] = "pending"
    country: Optional[str]

class PayeeCreate(PayeeBase):
    user_id: int

class Payee(PayeeBase):
    id: int
    user_id: int
    created_at: datetime

    class ConfigDict:
       from_attributes = True
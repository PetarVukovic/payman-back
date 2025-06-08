from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String)
    telegram_chat_id = Column(String)
    subscription_plan = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    payees = relationship("Payee", back_populates="user")
    invoices = relationship("Invoice", back_populates="user")
    approvals = relationship("ApprovalRequest", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")


class Payee(Base):
    __tablename__ = "payees"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    supplier_name = Column(String)
    iban = Column(String)
    wallet_address = Column(String)
    kyc_status = Column(String, default="pending")
    country = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="payees")
    invoices = relationship("Invoice", back_populates="payee")
    approvals = relationship("ApprovalRequest", back_populates="payee")
    payments = relationship("Payment", back_populates="payee")


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    payee_id = Column(Integer, ForeignKey("payees.id"))
    invoice_number = Column(String)
    invoice_file_url = Column(String)
    amount = Column(Numeric(12, 2))
    currency = Column(String(10))
    due_date = Column(DateTime)
    parsing_status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="invoices")
    payee = relationship("Payee", back_populates="invoices")
    approvals = relationship("ApprovalRequest", back_populates="invoice")
    payments = relationship("Payment", back_populates="invoice")


class ApprovalRequest(Base):
    __tablename__ = "approval_requests"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    payee_id = Column(Integer, ForeignKey("payees.id"))
    status = Column(String, default="pending")  # pending, approved, rejected, scheduled
    approved_at = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    invoice = relationship("Invoice", back_populates="approvals")
    user = relationship("User", back_populates="approvals")
    payee = relationship("Payee", back_populates="approvals")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    payee_id = Column(Integer, ForeignKey("payees.id"))
    amount = Column(Numeric(12, 2))
    currency = Column(String(10))
    payment_status = Column(String, default="pending")  # pending, processing, paid, failed
    payman_tx_id = Column(String)
    executed_at = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    invoice = relationship("Invoice", back_populates="payments")
    payee = relationship("Payee", back_populates="payments")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_type = Column(String)
    data = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="audit_logs")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    stripe_subscription_id = Column(String)
    plan = Column(String)
    trial_end = Column(DateTime)
    status = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="subscriptions")
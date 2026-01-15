
# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-13 00:45:00
import uuid
from sqlalchemy import Column, String, Integer, BigInteger, DateTime, ForeignKey, Numeric, JSON, Index, UniqueConstraint, Identity
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.core import GUID

class FinancialLedger(Base):
    """
    FINANCIAL LEDGER (L7) - HARDENED
    Garante imutabilidade e sequência via IDENTITY nativo do Postgres.
    """
    __tablename__ = "financial_ledger"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    # FIX: Uso de Identity para garantir geração automática no Postgres
    sequence_id = Column(BigInteger, Identity(always=True), unique=True, nullable=False)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False, index=True)
    
    entry_type = Column(String(10), nullable=False) 
    amount = Column(BigInteger, nullable=False)
    balance_after = Column(BigInteger, nullable=False)
    
    category = Column(String(50), nullable=False)
    description = Column(String(255))
    reference_id = Column(String(100), index=True)
    
    integrity_hash = Column(String(64), nullable=False)
    metadata_json = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    __table_args__ = (
        Index("idx_ledger_integrity_chain", "sequence_id", "integrity_hash"),
    )

class CustomerWallet(Base):
    __tablename__ = "customer_wallets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    balance = Column(Numeric(10, 2), default=0.00)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    company = relationship("Company", back_populates="wallets")
    __table_args__ = (Index("idx_wallet_unique", "company_id", "customer_phone", unique=True),)

class ServiceFeeLedger(Base):
    __tablename__ = "service_fee_ledger"
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    order_id = Column(GUID(), ForeignKey("orders.id"), nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    company = relationship("Company", back_populates="service_ledger")
    employee = relationship("Employee", back_populates="tips")

class DriverLedger(Base):
    __tablename__ = "driver_ledger"
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    order_id = Column(GUID(), ForeignKey("orders.id"), nullable=True)
    type = Column(String(50), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    company = relationship("Company", back_populates="driver_ledger")
    driver = relationship("Employee", back_populates="driver_transactions")
    order = relationship("Order", back_populates="driver_ledger_entries")

class PaymentTransaction(Base):
    __tablename__ = "payment_transactions"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    order_id = Column(GUID(), ForeignKey("orders.id"), nullable=False)
    provider = Column(String(50), nullable=False)
    external_id = Column(String(255), nullable=False)
    status = Column(String(50))
    amount = Column(Numeric(10, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (UniqueConstraint('provider', 'external_id', name='uq_payment_provider_id'),)


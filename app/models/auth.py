
# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-11 07:05:00

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.core import GUID, UserRole

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    role = Column(String(50), default=UserRole.KITCHEN.value, nullable=False) # Enum as String
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company", back_populates="employees")
    deliveries = relationship("Order", back_populates="driver")
    tips = relationship("ServiceFeeLedger", back_populates="employee", cascade="all, delete-orphan")
    driver_transactions = relationship("DriverLedger", back_populates="driver", cascade="all, delete-orphan")

    __table_args__ = (Index("idx_employee_email", "email", unique=True),)

class UserDevice(Base):
    __tablename__ = "user_devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    fcm_token = Column(String(255), nullable=False, unique=True)
    platform = Column(String(20), default="android")
    device_name = Column(String(100), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())


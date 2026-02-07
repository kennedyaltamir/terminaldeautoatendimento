# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-02-05 00:12:00
"""//
/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 2.4.0
 * OBJETIVO: Modelos de autoridade, dispositivos e persistência de Refresh Tokens.
 * Comportamento esperado: Adicionado relacionamento 'deliveries' para compatibilidade com Orders.
 */
//
"""
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
    role = Column(String(50), default=UserRole.KITCHEN.value, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    company = relationship("Company", back_populates="employees")
    refresh_tokens = relationship("UserRefreshToken", back_populates="user", cascade="all, delete-orphan")
    
    # 🛡️ FIX CRÍTICO: Relacionamento necessário para o módulo de Logística e iFood
    # Resolve o erro: Mapper 'Mapper[Employee(employees)]' has no property 'deliveries'
    deliveries = relationship("Order", back_populates="driver", foreign_keys="Order.driver_id")
    
    # Relacionamentos Financeiros
    tips = relationship("ServiceFeeLedger", back_populates="employee")
    driver_transactions = relationship("DriverLedger", back_populates="driver")
    shifts = relationship("DriverShift", back_populates="driver")

    __table_args__ = (Index("idx_employee_email", "email", unique=True),)

class UserRefreshToken(Base):
    __tablename__ = "user_refresh_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    jti = Column(String(64), unique=True, index=True, nullable=False)
    token_hash = Column(String(255), nullable=False)
    
    # Metadata para Auditoria Forense
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    last_used_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked = Column(Boolean, default=False)

    user = relationship("Employee", back_populates="refresh_tokens")

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
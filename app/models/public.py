
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.core import GUID

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, index=True)
    source = Column(String(50), default="landing_page")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class OrderFeedback(Base):
    __tablename__ = "order_feedbacks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(GUID(), ForeignKey("orders.id"), unique=True, nullable=False)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    score = Column(Integer, nullable=False) 
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    order = relationship("Order", back_populates="feedback")
    company = relationship("Company", back_populates="feedbacks")

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String(255), nullable=False, index=True)
    token = Column(String(64), nullable=False, unique=True, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# DOMAIN: BACKEND / MODELS
# VERSION: 2.1.0 (Logistics Initialized)
# DESCRIPTION: Modelos para Turnos, Jornadas e Telemetria de Motoristas.

import enum
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float, JSON, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base
from app.models.core import GUID

class JourneyStatus(str, enum.Enum):
    ASSIGNED = "ASSIGNED"
    EN_ROUTE_PICKUP = "EN_ROUTE_PICKUP"
    AT_PICKUP = "AT_PICKUP"
    EN_ROUTE_DELIVERY = "EN_ROUTE_DELIVERY"
    AT_DESTINATION = "AT_DESTINATION"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"
    INCIDENT = "INCIDENT"

class DriverShift(Base):
    __tablename__ = "driver_shifts"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    driver_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)
    total_online_minutes = Column(Integer, default=0)
    total_earnings = Column(Float, default=0.0)
    battery_start_level = Column(Float, nullable=True)
    vehicle_id = Column(String(50), nullable=True)

    driver = relationship("Employee", back_populates="shifts")
    journeys = relationship("LogisticsJourney", back_populates="shift")

class LogisticsJourney(Base):
    __tablename__ = "logistics_journeys"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    shift_id = Column(GUID(), ForeignKey("driver_shifts.id"), nullable=False)
    order_id = Column(GUID(), ForeignKey("orders.id"), nullable=False, unique=True)
    driver_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False) # ADICIONE ESTA LINHA
    status = Column(String(50), default=JourneyStatus.ASSIGNED.value, nullable=False) 
    accepted_at = Column(DateTime(timezone=True), server_default=func.now())
    pickup_at = Column(DateTime(timezone=True), nullable=True)
    arrival_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    distance_km = Column(Float, default=0.0)
    delivery_fee = Column(Float, default=0.0)
    tip_amount = Column(Float, default=0.0)
    pod_code_input = Column(String(10), nullable=True)
    pod_location_lat = Column(Float, nullable=True)
    pod_location_lng = Column(Float, nullable=True)

    shift = relationship("DriverShift", back_populates="journeys")
    telemetry = relationship("DriverTelemetry", back_populates="journey")

class DriverTelemetry(Base):
    __tablename__ = "driver_telemetry"
    id = Column(Integer, primary_key=True, autoincrement=True)
    journey_id = Column(GUID(), ForeignKey("logistics_journeys.id"), nullable=True)
    driver_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    speed = Column(Float, nullable=True)
    heading = Column(Float, nullable=True)
    accuracy = Column(Float, nullable=True)
    battery_level = Column(Float, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    journey = relationship("LogisticsJourney", back_populates="telemetry")

    __table_args__ = (
        Index('idx_telemetry_driver_time', 'driver_id', 'timestamp'),
        Index('idx_telemetry_journey_time', 'journey_id', 'timestamp'),
    )

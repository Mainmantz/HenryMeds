from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, String, Date, Time, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from database import Base

class ProviderAvailability(Base):
    __tablename__ = "provider_availability"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_name = Column(String, index=True)
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)

class AppointmentSlot(Base):
    __tablename__ = "appointment_slots"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_name = Column(String, index=True)
    date = Column(Date)
    time = Column(Time)

class Reservation(Base):
    __tablename__ = "reservations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slot_id = Column(UUID(as_uuid=True), ForeignKey("appointment_slots.id"))
    client_name = Column(String)
    confirmed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())

    slot = relationship("AppointmentSlot")

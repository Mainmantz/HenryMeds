from pydantic import BaseModel
from datetime import date, time
from typing import List
from uuid import UUID

class ProviderAvailabilitySchema(BaseModel):
    provider_name: str
    date: date
    start_time: time
    end_time: time

class AppointmentSlotSchema(BaseModel):
    id: UUID
    provider_name: str
    date: date
    time: time

class ReservationRequestSchema(BaseModel):
    slot_id: str
    client_name: str
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, select
from datetime import datetime, timedelta
import uuid
from models.models import ProviderAvailability, AppointmentSlot
from models.schemas import ProviderAvailabilitySchema
from database import get_session

router = APIRouter()

@router.post("/providers/availability")
async def submit_availability(availability: ProviderAvailabilitySchema, session: Session = Depends(get_session)):
    existing_availability = session.execute(
        select(ProviderAvailability).where(
            ProviderAvailability.provider_name == availability.provider_name,
            ProviderAvailability.date == availability.date,
            and_(
                ProviderAvailability.start_time <= availability.end_time,
                ProviderAvailability.end_time >= availability.start_time
            )
        )
    ).scalars().first()
    
    if existing_availability:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Availability already exists for the given date and time range")
    
    provider_availability = ProviderAvailability(
        provider_name=availability.provider_name,
        date=availability.date,
        start_time=availability.start_time,
        end_time=availability.end_time
    )
    session.add(provider_availability)
    
    # Generate 15-minute slots
    current_time = datetime.combine(availability.date, availability.start_time)
    end_time = datetime.combine(availability.date, availability.end_time)
    
    while current_time < end_time:
        slot_time = current_time.time()
        slot = AppointmentSlot(
            provider_name=availability.provider_name,
            date=availability.date,
            time=slot_time,
            id=uuid.uuid4()
        )
        session.add(slot)
        current_time += timedelta(minutes=15)
    
    session.commit()
    
    return {"message": "Availability submitted successfully"}
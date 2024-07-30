from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timedelta
import uuid
from typing import List, Optional
from models.models import AppointmentSlot, Reservation
from models.schemas import AppointmentSlotSchema, ReservationRequestSchema
from database import get_session
from services import reservations

router = APIRouter()

@router.get("/appointments/slots", response_model=List[AppointmentSlotSchema])
async def get(provider_name: Optional[str] = None, date: Optional[str] = None, session: Session = Depends(get_session)):
    query = select(AppointmentSlot).outerjoin(Reservation).where(Reservation.id == None)

    if provider_name:
        query = query.where(AppointmentSlot.provider_name == provider_name)
    if date:
        query = query.where(AppointmentSlot.date == datetime.strptime(date, "%Y-%m-%d").date())
        
    slots = session.execute(query).scalars().all()
    return slots

@router.post("/appointments/reserve")
async def create(reservation_request: ReservationRequestSchema, session: Session = Depends(get_session)):
    slot = session.get(AppointmentSlot, reservation_request.slot_id)
    if not slot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Slot not found")
    
    existing_reservation = session.execute(
        select(Reservation).where(Reservation.slot_id == slot.id)
    ).scalars().first()
    
    if existing_reservation:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Slot already reserved")
    
    if datetime.combine(slot.date, slot.time) <= datetime.now() + timedelta(hours=24):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reservations must be made at least 24 hours in advance")

    reservation = Reservation(
        id=uuid.uuid4(),
        slot_id=reservation_request.slot_id,
        client_name=reservation_request.client_name,
        confirmed=False,
        created_at=datetime.now(),
    )

    session.add(reservation)
    session.commit()
    
    return {"reservation_id": str(reservation.id), "message": "Slot reserved successfully"}

@router.patch("/appointments/{reservation_id}/confirm")
async def confirm_reservation(reservation_id: str, session: Session = Depends(get_session)):
    reservation = session.get(Reservation, reservation_id)
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    
    if reservation.confirmed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reservation already confirmed")
    
    expiration_time = reservation.created_at + timedelta(minutes=30)
    if datetime.now() > expiration_time:
        session.delete(reservation)
        session.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reservations must be confirmed within 30 minutes, this will be deleted, please rebook")
    
    reservation.confirmed = True
    session.commit()
    
    return {"message": "Reservation confirmed successfully"}
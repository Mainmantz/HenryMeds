from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timedelta
from database import engine
from models.models import Reservation

def expire_reservations():
    print("expring reservations")
    with Session(engine) as session:
        expiration_time = datetime.now() - timedelta(minutes=30)
        expired_reservations = session.execute(
            select(Reservation).where(
                Reservation.confirmed == False,
                Reservation.created_at < expiration_time
            )
        ).scalars().all()
        
        for reservation in expired_reservations:
            session.delete(reservation)
        
        session.commit()
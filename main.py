from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import database, engine, Base
from routes import appointments, providers
from services import reservations
from apscheduler.schedulers.background import BackgroundScheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(reservations.expire_reservations, trigger="cron", minute="15")
    scheduler.start()

    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

Base.metadata.create_all(bind=engine)

@app.get("/")
def health():
    return "App is healthy"

app.include_router(appointments.router)
app.include_router(providers.router)
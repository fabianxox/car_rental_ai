from fastapi import FastAPI
from app.api.webhook import router as webhook_router

app = FastAPI()

app.include_router(webhook_router)
from app.services.scheduler import scheduler


@app.on_event("startup")
async def startup_event():

    scheduler.start()

    print("SCHEDULER STARTED")


@app.get("/")
def root():

    return {
        "message": "Car Rental AI Backend Running"
    }
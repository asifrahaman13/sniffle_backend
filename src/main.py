import logging
import threading
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
import asyncio
import schedule
from src.internal.interfaces.data_interface import DataInterface
from src.internal.use_cases.data_service import DataService
from src.infastructure.middleware.logging_middleware import (
    log_middleware,
)
from src.application.web.controllers.socket_controller import websocket_router
from src.application.web.controllers.auth_controller import auth_router
from src.application.web.controllers.data_controller import data_router
from src.application.web.controllers.voice_controller import voice_router
from src.application.web.controllers.wearable_controller import wearable_router


data_service = DataService()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

# Allow from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(websocket_router, prefix="/websocket", tags=["websocket connection "])
app.include_router(auth_router, prefix="/auth", tags=["Auth router"])
app.include_router(data_router, prefix="/data", tags=["Data router"])
app.include_router(voice_router, prefix="/voice", tags=["Voice router"])
app.include_router(wearable_router, prefix="/wearable", tags=["Wearable router"])

# Include the middleware.
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

# Define the jobs
def job():
    print("I'm working...")
    data_interface: DataInterface = data_service
    data_interface.schedule_recommendations()
    print("Recommendations scheduled")

# Schedule the jobs
# schedule.every(30).seconds.do(job)
# schedule.every().day.at("10:30").do(job)

def scheduler_thread():
    async def run_scheduler():
        while True:
            schedule.run_pending()
            await asyncio.sleep(1)

    asyncio.run(run_scheduler())


# Start the scheduler thread
scheduler = threading.Thread(target=scheduler_thread, daemon=True)
scheduler.start()

# Health check endpoint
@app.get("/health")
async def health_check():
    return JSONResponse(status_code=200, content={"status": "healthy"})
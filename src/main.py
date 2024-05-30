from contextlib import asynccontextmanager
import logging
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

# Include the middleware.
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)


# Define the jobs
def job():
    print("I'm working...")
    data_interface: DataInterface = data_service
    data_interface.schedule_recommendations()
    logging.info("Recommendations scheduled")


# def job_with_argument(name):
#     print(f"I am {name}")

# Schedule the jobs
# schedule.every(10).seconds.do(job)
# schedule.every(1).minutes.do(job)
# schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().day.at("12:42", "Europe/Amsterdam").do(job)
# schedule.every().minute.at(":17").do(job)
# schedule.every(10).seconds.do(job_with_argument, name="Peter")


# Function to run the scheduler
async def run_scheduler():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the scheduler in the background
    loop = asyncio.get_event_loop()
    task = loop.create_task(run_scheduler())

    # Yield control back to FastAPI
    yield

    # Cancel the scheduler task
    task.cancel()
    await task


# Use the lifespan context
app.router.lifespan_context = lifespan


# Health check endpoint
@app.get("/health")
async def health_check():
    return JSONResponse(status_code=200, content={"status": "healthy"})

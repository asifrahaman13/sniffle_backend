import logging
import threading
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
import asyncio
import schedule
from src.internal.interfaces.data_interface import DataInterface
from src.infastructure.middleware.logging_middleware import PrefixMiddleware
from math import ceil
import redis.asyncio as redis
import uvicorn
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi import status
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import os
from config.config import REDIS_URL
from src.application.web.controllers.socket_controller import websocket_router
from src.application.web.controllers.auth_controller import auth_router
from src.application.web.controllers.data_controller import data_router
from src.application.web.controllers.voice_controller import voice_router
from src.application.web.controllers.wearable_controller import wearable_router
from src.application.web.controllers.fhir_controller import fhir_router
from exports.exports import search_repository, data_service

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def client_identifier(request: Request):
    return request.client.host


async def custom_callback(request: Request, response: Response, pexpire: int):
    """
    Default callback when too many requests
    :param request:
    :param pexpire: The remaining milliseconds
    :param response:
    :return:
    """
    expire = ceil(pexpire / 1000)
    raise HTTPException(
        status.HTTP_429_TOO_MANY_REQUESTS,
        f"Too Many Requests. Retry after {expire} seconds.",
        headers={"Retry-After": str(expire)},
    )


@asynccontextmanager
async def lifespan(_: FastAPI):

    # Initialize Qdrant
    # search_repository.initialize_qdrant()

    redis_connection = redis.from_url(REDIS_URL, encoding="utf8")
    await FastAPILimiter.init(
        redis=redis_connection,
        identifier=client_identifier,
        http_callback=custom_callback,
    )
    yield
    await FastAPILimiter.close()


app = FastAPI(lifespan=lifespan)

# Allow from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(
    websocket_router,
    prefix="/websocket",
    tags=["websocket connection"],
)
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth router"],
    dependencies=[
        Depends(RateLimiter(times=10, seconds=10, identifier=client_identifier))
    ],
)
app.include_router(
    data_router,
    prefix="/data",
    tags=["Data router"],
    dependencies=[
        Depends(RateLimiter(times=10, seconds=10, identifier=client_identifier))
    ],
)
app.include_router(voice_router, prefix="/voice", tags=["Voice router"])
app.include_router(wearable_router, prefix="/wearable", tags=["Wearable router"])
app.include_router(
    fhir_router,
    prefix="/fhir",
    tags=["FHIR router"],
    dependencies=[
        Depends(RateLimiter(times=10, seconds=10, identifier=client_identifier))
    ],
)


# Include the middleware
app.add_middleware(PrefixMiddleware)


# Define the jobs
def job():
    logging.info("Recommendations scheduled")
    data_interface: DataInterface = data_service
    data_interface.schedule_recommendations()
    logging.info("All scheduling done...")


# Schedule the jobs
# schedule.every(30).seconds.do(job)
schedule.every().day.at("10:30").do(job)


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
@app.get(
    "/health",
    dependencies=[
        Depends(RateLimiter(times=10, seconds=10, identifier=client_identifier))
    ],
)
async def health_check(request: Request):
    ip = request.client.host
    logging.info(f"Request from IP: {ip}")
    return JSONResponse(status_code=200, content={"status": "healthy"})


@app.get("/")
async def health_check():
    return JSONResponse(
        status_code=200,
        content={"status": "The server is running as expected."},
    )


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    logging.info(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

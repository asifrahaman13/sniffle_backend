import logging
from fastapi import FastAPI
from src.application.web.controllers.socket_controller import websocket_router
from src.application.web.controllers.auth_controller import auth_router
from src.application.web.controllers.data_controller import data_router
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from src.infastructure.middleware.logging_middleware import (
    log_middleware,
)
from starlette.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()

# Allow from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(
    websocket_router, prefix="/websocket", tags=["websocket connection "]
)
app.include_router(auth_router, prefix="/auth", tags=["Auth router"])
app.include_router(data_router, prefix="/data", tags=["Data router"])

# Include the middleware.
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)


# Health check endpoint
@app.get("/health")
async def health_check():
    return JSONResponse(status_code=200, content={"status": "healthy"})

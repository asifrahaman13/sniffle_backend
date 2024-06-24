import logging
import time
from fastapi import WebSocket
import asyncio
from fastapi import APIRouter
from exports.exports import manager
from src.internal.interfaces.auth_interface import AuthInterface
from fastapi import Depends
from exports.exports import auth_service

wearable_router = APIRouter()


def glucose_monitor(value: float):
    if value > 100:
        return True


def heart_rate_monitor(value: int):
    if value < 60 or value > 100:
        return True


def blood_pressure_monitor(value: int):
    if value > 140 or value < 60:
        return True


def temperature_monitor(value: float):
    if value > 100.4 or value < 97:
        return True


@wearable_router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    user_id: str,
    websocket: WebSocket,
    auth_interface: AuthInterface = Depends(auth_service),
):

    user_info = auth_interface.decode_access_token(user_id)
    logging.info(user_info)

    if "error" in user_info:
        await manager.disconnect(websocket)
        return

    try:
        logging.info(f"Client #{user_id} connected for health metrics")
        await manager.connect(websocket, user_id, connection_type="wearable")
        while True:
            data = await websocket.receive_json()

            await manager.send_personal_message(
                "You are connected to the server",
                websocket,
            )
            # Glucose Level Monitoring
            if "glucoseLevel" in data:
                glucose_level = float(data["glucoseLevel"])
                logging.info(
                    f"Received glucose level data from user {user_id}: {glucose_level}"
                )
                if glucose_monitor(glucose_level):
                        logging.info("Glucose level alert")
                        logging.info("Push notification sent")
                        await manager.send_personal_message(
                            "Hey your current glucose level: {} is unusual. Please take care.".format(
                                data["glucoseLevel"]
                            ),
                            websocket,
                        )
                        await asyncio.sleep(1)

            # Heart Rate Monitoring
            if "heartRate" in data:
                heart_rate = int(data["heartRate"])
                logging.info(
                    f"Received heart rate data from user {user_id}: {heart_rate}"
                )
                if heart_rate_monitor(heart_rate):
                        logging.info("Heart rate alert")
                        logging.info("Push notification sent")
                        await manager.send_personal_message(
                            "Hey your current heart rate level: {} is unusual. Please take care.".format(
                                data["heartRate"]
                            ),
                            websocket,
                        )
                        await asyncio.sleep(1)

            # Blood Pressure Monitoring
            if "bloodPressure" in data:
                blood_pressure = int(data["bloodPressure"])
                logging.info(
                    f"Received blood pressure data from user {user_id}: {blood_pressure}"
                )
                if blood_pressure_monitor(blood_pressure):
                        logging.info("Blood pressure alert")
                        logging.info("Push notification sent")
                        await manager.send_personal_message(
                            "Hey your current blood pressure level: {} is unusual. Please take care.".format(
                                data["bloodPressure"]
                            ),
                            websocket,
                        )
                        await asyncio.sleep(1)

            # Temperature Monitoring
            if "temperature" in data:
                temperature = float(data["temperature"])
                logging.info(
                    f"Received temperature data from user {user_id}: {temperature}"
                )
                if temperature_monitor(temperature):
                        logging.info("Temperature alert")
                        logging.info("Push notification sent")
                        await manager.send_personal_message(
                            "Hey your current temperature level: {} is unusual. Please take care.".format(
                                data["temperature"]
                            ),
                            websocket,
                        )
                        await asyncio.sleep(1)
    except Exception as e:
        await manager.disconnect(websocket, "wearable")

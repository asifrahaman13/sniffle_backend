import logging
import time
from fastapi import WebSocket
import asyncio
from fastapi import APIRouter

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


@wearable_router.websocket("/ws/{id}")
async def websocket_endpoint(id: str, websocket: WebSocket):
    logging.info(f"Client #{id} connected for health metrics")
    await websocket.accept()
    last_time = int(time.time())
    while True:
        data = await websocket.receive_json()
        user_id = id
        # Glucose Level Monitoring
        if "glucoseLevel" in data:
            glucose_level = float(data["glucoseLevel"])
            logging.info(
                f"Received glucose level data from user {user_id}: {glucose_level}"
            )
            if glucose_monitor(glucose_level):
                if int(time.time()) - last_time > 60:
                    logging.info("Glucose level alert")
                    logging.info("Push notification sent")
                    await websocket.send_text(
                        f"Hey your current glucose level: {data["glucoseLevel"]} is unusual. Please take care."
                    )
                    await asyncio.sleep(1)
                    last_time = int(time.time())

        # Heart Rate Monitoring
        if "heartRate" in data:
            heart_rate = int(data["heartRate"])
            logging.info(f"Received heart rate data from user {user_id}: {heart_rate}")
            if heart_rate_monitor(heart_rate):
                if int(time.time()) - last_time > 60:
                    logging.info("Heart rate alert")
                    logging.info("Push notification sent")
                    await websocket.send_text(
                        f"Hey your current heart rate level: {data["heartRate"]} is unusual. Please take care."
                    )
                    await asyncio.sleep(1)
                    last_time = int(time.time())

        # Blood Pressure Monitoring
        if "bloodPressure" in data:
            blood_pressure = int(data["bloodPressure"])
            logging.info(
                f"Received blood pressure data from user {user_id}: {blood_pressure}"
            )
            if blood_pressure_monitor(blood_pressure):
                if int(time.time()) - last_time > 60:
                    logging.info("Blood pressure alert")
                    logging.info("Push notification sent")
                    await websocket.send_text(
                        f"Hey your current blood pressure level: {data["bloodPressure"]} is unusual. Please take care."
                    )
                    await asyncio.sleep(1)
                    last_time = int(time.time())

        # Temperature Monitoring
        if "temperature" in data:
            temperature = float(data["temperature"])
            logging.info(
                f"Received temperature data from user {user_id}: {temperature}"
            )
            if temperature_monitor(temperature):
                if int(time.time()) - last_time > 60:
                    logging.info("Temperature alert")
                    logging.info("Push notification sent")
                    await websocket.send_text(
                        f"Hey your current temperature level: {data["temperature"]} is unusual. Please take care."
                    )
                    await asyncio.sleep(1)
                    last_time = int(time.time())

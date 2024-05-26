from pydantic import BaseModel, Field


class HealthData(BaseModel):
    heart_rate: int = Field(description="The heart rate in beats per minute")
    systol_blood_pressure: str = Field(
        description="The systol blood pressure as systolic/diastolic in mmHg"
    )
    diastol_blood_pressure: str = Field(
        description="The diastol blood pressure as systolic/diastolic in mmHg"
    )
    respiratory_rate: int = Field(
        description="The respiratory rate in breaths per minute"
    )
    body_temperature: float = Field(
        description="The body temperature in degrees Celsius"
    )

    step_count: int = Field(
        description="The number of steps taken by the user in the day"
    )
    calories_burned: int = Field(
        description="The number of calories burned by the user in the day"
    )
    distance_travelled: int = Field(
        description="The distance travelled by the user in the day"
    )
    sleep_duration: int = Field(description="The duration of sleep in hours")
    water_consumed: int = Field(description="The amount of water consumed in litres")
    caffeine_consumed: int = Field(description="The amount of caffeine consumed in mg")
    alcohol_consumed: int = Field(description="The amount of alcohol consumed in units")

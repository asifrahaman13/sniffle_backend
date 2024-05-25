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
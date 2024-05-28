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


class Recommendations(BaseModel):
    medications_recommended: str = Field(
        description="Medications recommended based on health data"
    )
    diet_recommended: str = Field(
        description="Diet recommended based on health data"
    )
    exercise_recommended: str = Field(
        description="Exercise recommended based on health data"
    )
    lifestyle_changes_recommended: str = Field(
        description="Lifestyle changes recommended based on health data"
    )
    stress_management_techniques_recommended: str = Field(
        description="Stress management techniques recommended based on health data"
    )
    sleep_hygiene_techniques_recommended: str = Field(
        description="Sleep hygiene techniques recommended based on health data"
    )
    mental_health_techniques_recommended: str = Field(
        description="Mental health techniques recommended based on health data"
    )
    relaxation_techniques_recommended: str = Field(
        description="Relaxation techniques recommended based on health data"
    )
    social_support_techniques_recommended: str = Field(
        description="Social support techniques recommended based on health data"
    )
    other_recommendations: str = Field(
        description="Other recommendations based on health data"
    )

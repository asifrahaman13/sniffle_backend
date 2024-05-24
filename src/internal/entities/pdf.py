from pydantic import BaseModel

# Both fields should be madnatory.
class Pdf(BaseModel):
    question: str
    filename: str 
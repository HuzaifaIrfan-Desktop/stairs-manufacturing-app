import pydantic
from pydantic import BaseModel

class CalculatorOutputResults(BaseModel):
    result: float
    error: str
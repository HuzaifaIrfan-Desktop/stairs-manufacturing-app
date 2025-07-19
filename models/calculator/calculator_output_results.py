import pydantic
from pydantic import BaseModel

class CalculatorOutputResults(BaseModel):
    result: float
    error: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        use_enum_values = True
        extra = "forbid"
        
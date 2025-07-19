import pydantic
from pydantic import BaseModel

class JobInputParams(BaseModel):
    job_id: int
    job_name: str
    job_description: str
    job_priority: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        use_enum_values = True
        extra = "forbid"
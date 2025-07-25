
from pydantic import BaseModel, Field, model_validator

class PartParams(BaseModel):
    job_name: str = Field(..., description="Name of the Job")
    part_name: str = Field(..., description="Name of the part")



    @model_validator(mode='after')
    def compute(self) -> 'PartParams':
        return self

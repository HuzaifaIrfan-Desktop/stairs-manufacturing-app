
from pydantic import BaseModel, Field

class PartParams(BaseModel):
    job_name: str = Field(..., description="Name of the Job")
    part_name: str = Field(..., description="Name of the part")


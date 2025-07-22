
from pydantic import BaseModel, Field

class DrawingParams(BaseModel):
    job_name: str = Field(..., description="Name of the Job")
    drawing_name: str = Field(..., description="Name of the drawing")


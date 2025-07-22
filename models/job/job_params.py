import pydantic
from pydantic import BaseModel

class JobInputParams(BaseModel):
    job_name: str
    builder_name: str


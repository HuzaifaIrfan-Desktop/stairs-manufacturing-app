


from pydantic import BaseModel, Field

class AssemblyParams(BaseModel):
    job_name: str = Field(..., description="Name of the Job")
    assembly_name: str = Field(..., description="Name of the assembly")

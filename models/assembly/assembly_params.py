


from pydantic import BaseModel, Field, model_validator

class AssemblyParams(BaseModel):
    job_name: str = Field(..., description="Name of the Job")
    assembly_name: str = Field(..., description="Name of the assembly")
    builder_name: str = Field(..., description="Name of the builder")



    @model_validator(mode='after')
    def compute(self) -> 'AssemblyParams':
        return self
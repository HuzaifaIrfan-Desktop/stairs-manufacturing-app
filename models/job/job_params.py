import pydantic
from pydantic import BaseModel, Field, model_validator

class JobInputParams(BaseModel):
    job_class_name: str = Field(init=False, default=None, validate_default=False, description="Job class name")
    job_name: str = "Default Job"
    builder_name: str = "Default Builder"


    @model_validator(mode='after')
    def compute_params(self) -> 'JobInputParams':

        if self.job_class_name is None:
            classes=[c.__qualname__ for c in self.__class__.__mro__ if c is not BaseModel and c is not object]
            # print(f"Setting job_class_name to {classes}")
            self.job_class_name = classes[0]

        return self

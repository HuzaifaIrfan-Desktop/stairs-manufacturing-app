import pydantic
from pydantic import BaseModel, Field, model_validator

class JobInputParams(BaseModel):
    job_template: str = Field(init=False, default="JobInputParams", validate_default=False, description="Job template class names")
    job_name: str = "Default Job"
    builder_name: str = "Default Builder"


    @model_validator(mode='after')
    def compute_params(self) -> 'JobInputParams':
        # if self.job_template is None:
        classes=[c.__qualname__ for c in self.__class__.__mro__ if c is not BaseModel and c is not object]
        print(f"Setting job_template to {classes}")
        self.job_template = classes[0]

        return self

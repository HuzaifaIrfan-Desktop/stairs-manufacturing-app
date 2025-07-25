import pydantic
from pydantic import BaseModel, Field, model_validator
from typing import Any

class JobInputParams(BaseModel):
    job_class_name: str = Field(init=False, default=None, validate_default=False, description="Job class name")
    job_name: str = Field(default="Default Standard Stairs Job", description="Job name")
    builder_name: str = Field(default="Default Builder", description="Builder name")


    # @model_validator(mode='before')
    # def compute_job_class_name(self) -> 'JobInputParams':

    #     if self.job_class_name is None:
    #         classes=[c.__qualname__ for c in self.__class__.__mro__ if c is not BaseModel and c is not object]
    #         # print(f"Setting job_class_name to {classes}")
    #         self.job_class_name = classes[0]

    #     return self

    @model_validator(mode='before')
    @classmethod
    def compute_job_class_name(cls, data: Any) -> Any:
        if isinstance(data, dict) and data.get('job_class_name') is None:
            classes = [
                c.__qualname__
                for c in cls.__mro__
                if c is not BaseModel and c is not object
            ]
            data['job_class_name'] = classes[0]
        return data

    @model_validator(mode='after')
    def compute(self) -> 'JobInputParams':
        return self


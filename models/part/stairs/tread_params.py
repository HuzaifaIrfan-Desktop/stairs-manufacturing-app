
from models.part.part_params import PartParams
from pydantic import BaseModel, Field, model_validator

from models.material.lumber import Lumber
from models.material.plywood import Plywood, plywood_1
from typing import Union as union
from models.material.material import Material

class TreadParams(PartParams):
    tread_depth: float = Field(..., gt=0, description="Depth of the tread, must be positive and non-zero")
    tread_thickness: float = Field(default=None, gt=0, description="Thickness of the tread, must be positive and non-zero")
    tread_length: float = Field(..., gt=0, description="Length of the tread, must be positive and non-zero")

    tread_material: union[Lumber, Plywood] = Field(default=plywood_1, description="Material of the tread, e.g., Lumber, Plywood, etc.")


    @model_validator(mode='after')
    def compute(self) -> 'TreadParams':
        if self.tread_thickness is None:
            self.tread_thickness = self.tread_material.thickness
        return self

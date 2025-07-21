from pydantic import BaseModel, Field, model_validator

from models.material.lumber import Lumber
from models.material.plywood import Plywood, plywood_3_8
from typing import Union as union
from models.material.material import Material
from models.part.part_params import PartParams

class RiserParams(PartParams):
    riser_height: float = Field(..., gt=0, description="Height of the riser, must be positive and non-zero")
    riser_thickness: float = Field(init=False, default=None, validate_default=False, gt=0, description="Thickness of the riser, must be positive and non-zero")
    riser_length: float = Field(..., gt=0, description="Length of the riser, must be positive and non-zero")

    material: union[Lumber, Plywood] = Field(default=plywood_3_8, description="Material of the tread, e.g., Lumber, Plywood, etc.")


    @model_validator(mode='after')
    def compute_params(self) -> 'RiserParams':
        if self.riser_thickness is None:
            self.riser_thickness = self.material.thickness
        return self

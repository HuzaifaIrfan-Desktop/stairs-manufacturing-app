
from models.part.part_params import PartParams
from pydantic import BaseModel, Field, model_validator

from models.material.lumber import Lumber
from models.material.plywood import Plywood, plywood_1
from typing import Union as union
from models.material.material import Material

class LandingParams(PartParams):
    landing_length: float = Field(..., gt=0, description="Length of the landing, must be positive and non-zero")
    landing_width: float = Field(..., gt=0, description="Width of the landing, must be positive and non-zero")
    landing_thickness: float = Field(default=2, gt=0, description="Thickness of the landing, must be positive and non-zero")
    
    landing_top_position: float = Field(..., ge=0, description="Top position of the landing, must be positive and non-zero")
    landing_x_position: float = Field(default=0, ge=0, description="X position of the landing, must be positive and non-zero")
    landing_y_position: float = Field(default=0, ge=0, description="Y position of the landing, must be positive and non-zero")

    @model_validator(mode='after')
    def compute(self) -> 'LandingParams':
        return self

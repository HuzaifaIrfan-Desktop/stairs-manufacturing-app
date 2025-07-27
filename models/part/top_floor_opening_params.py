
from models.part.part_params import PartParams
from pydantic import BaseModel, Field, model_validator

from models.material.lumber import Lumber
from models.material.plywood import Plywood, plywood_1
from typing import Union as union
from models.material.material import Material

class TopFloorOpeningParams(PartParams):
    opening_length: float = Field(..., gt=0, description="Length of the opening, must be positive and non-zero")
    opening_width: float = Field(..., gt=0, description="Width of the opening, must be positive and non-zero")

    opening_thickness: float = Field(default=2, gt=0, description="Thickness of the opening, must be positive and non-zero")
    opening_top_position: float = Field(..., ge=0, description="Top position of the opening, must be positive and non-zero")
    opening_x_position: float = Field(default=0, ge=0, description="X position of the opening, must be positive and non-zero")
    opening_y_position: float = Field(default=0, ge=0, description="Y position of the opening, must be positive and non-zero")
    
    opening_floor_outward_thickness: float = Field(default=5, gt=0, description="Thickness of the floor outward from the opening, must be positive and non-zero")

    @model_validator(mode='after')
    def compute(self) -> 'TopFloorOpeningParams':
        return self

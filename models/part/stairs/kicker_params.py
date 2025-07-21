from pydantic import BaseModel, Field, model_validator

from models.material.lumber import Lumber
from models.material.plywood import Plywood, plywood_1
from typing import Union as union
from models.material.material import Material
from models.part.part_params import PartParams

class KickerParams(PartParams):
    kicker_height: float = Field(..., gt=0, description="Height of the kicker, must be positive and non-zero")
    kicker_depth: float = Field(..., gt=0, description="Depth of the kicker, must be positive and non-zero")
    kicker_length: float = Field(..., gt=0, description="Length of the kicker, must be positive and non-zero")

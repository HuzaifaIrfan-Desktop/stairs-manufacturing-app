
from models.part.part_params import PartParams
from pydantic import Field

class TreadParams(PartParams):
    tread_depth: float = Field(..., gt=0, description="Depth of the tread, must be positive and non-zero")
    tread_thickness: float = Field(..., gt=0, description="Thickness of the tread, must be positive and non-zero")
    tread_length: float = Field(..., gt=0, description="Length of the tread, must be positive and non-zero")


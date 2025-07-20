
from pydantic import Field
from models.part.part_params import PartParams

class RiserParams(PartParams):
    riser_height: float = Field(..., gt=0, description="Height of the riser, must be positive and non-zero")
    riser_thickness: float = Field(..., gt=0, description="Thickness of the riser, must be positive and non-zero")
    riser_length: float = Field(..., gt=0, description="Length of the riser, must be positive and non-zero")


from models.material.material import Material
from pydantic import Field

class Plywood(Material):
    thickness: float = Field(..., gt=0, description="Thickness of the plywood, must be positive and non-zero")



plywood_1 = Plywood(material_name='1" Plywood', thickness=1.0)
plywood_3_8 = Plywood(material_name='3/8" Plywood', thickness=0.375)
plywood_5_8 = Plywood(material_name='5/8" Plywood', thickness=0.625)

available_plywoods = {
    '1" Plywood': plywood_1,
    '3/8" Plywood': plywood_3_8,
    '5/8" Plywood': plywood_5_8,
}



from models.material.material import Material
from pydantic import Field

class Lumber(Material):
    thickness: float = Field(..., gt=0, description="Thickness of the lumber, must be positive and non-zero")
    width: float = Field(..., gt=0, description="Width of the lumber, must be positive and non-zero")



lumber_2x6 = Lumber(material_name='2x6 Lumber', thickness=1.5, width=5.5)
lumber_2x8 = Lumber(material_name='2x8 Lumber', thickness=1.5, width=7.25)
lumber_2x10 = Lumber(material_name='2x10 Lumber', thickness=1.5, width=9.25)
lumber_2x12 = Lumber(material_name='2x12 Lumber', thickness=1.5, width=11.25)
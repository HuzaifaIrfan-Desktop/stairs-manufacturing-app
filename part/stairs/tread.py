

import cadquery as cq
from utils.math import inch_to_mm


from part.part import Part
from models.part.stairs.tread_params import TreadParams


class Tread(Part):
    def __init__(self, tread_params: TreadParams):
        print(f"Creating Tread with params: {tread_params}")
        self.tread_params = tread_params
        # _build is run by parent class Part and it uses self.tread_params
        # to create the part, so we call super().__init__ here
        super().__init__(tread_params)


    def calculate_area(self) -> float:
        return self.tread_params.tread_length * self.tread_params.tread_depth

    def calculate_volume(self) -> float:
        return self.calculate_area() * self.tread_params.tread_thickness

    def _build(self) -> cq.Workplane:
        # Create a simple tread part
        return (
                    cq.Workplane("XZ")
                    .rect(inch_to_mm(self.tread_params.tread_depth), inch_to_mm(self.tread_params.tread_thickness))
                    .extrude(inch_to_mm(self.tread_params.tread_length))
                )

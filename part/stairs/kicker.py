

import cadquery as cq
from utils.math import inch_to_mm


from part.part import Part
from models.part.stairs.kicker_params import KickerParams

class Kicker(Part):
    def __init__(self, kicker_params: KickerParams):
        print(f"Creating Kicker with params: {kicker_params}")
        self.kicker_params = kicker_params
        # _build is run by parent class Part and it uses self.kicker_params
        # to create the part, so we call super().__init__ here
        super().__init__(kicker_params)


    def calculate_area(self) -> float:
        return self.kicker_params.kicker_depth * self.kicker_params.kicker_height

    def calculate_volume(self) -> float:
        return self.calculate_area() * self.kicker_params.kicker_length

    def _build(self) -> cq.Workplane:
        # Create a simple kicker part
        return (
            cq.Workplane("XZ")
            .rect(inch_to_mm(self.kicker_params.kicker_depth), inch_to_mm(self.kicker_params.kicker_height))
            .extrude(inch_to_mm(self.kicker_params.kicker_length))
        )

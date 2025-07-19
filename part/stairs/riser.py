

import cadquery as cq
from utils.math import inch_to_mm


from part.part import Part
from models.part.stairs.riser_params import RiserParams


class Riser(Part):
    def __init__(self, riser_params: RiserParams):
        print(f"Creating Riser with params: {riser_params}")
        self.riser_params = riser_params
        # _build is run by parent class Part and it uses self.riser_params
        # to create the part, so we call super().__init__ here
        super().__init__(riser_params)


    def calculate_area(self) -> float:
        return self.riser_params.riser_length * self.riser_params.riser_height  

    def calculate_volume(self) -> float:
        return self.calculate_area() * self.riser_params.riser_thickness

    def _build(self) -> cq.Workplane:
        # Create a simple riser part
        return (
            cq.Workplane("YZ")
            .rect(inch_to_mm(self.riser_params.riser_thickness), inch_to_mm(self.riser_params.riser_height))
            .extrude(inch_to_mm(self.riser_params.riser_length))
        )

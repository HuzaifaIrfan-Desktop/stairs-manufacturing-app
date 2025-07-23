

import cadquery as cq
from utils.math import inch_to_mm

from logger import part_logger
# part_logger.info("Loading Riser class from part.stairs.riser module")

from part.part import Part
from models.part.stairs.riser_params import RiserParams


class Riser(Part):
    def __init__(self, riser_params: RiserParams):
        part_logger.info(f"Creating Riser with params: {riser_params}")
        self.part_params = riser_params
        # _build is run by parent class Part and it uses self.riser_params
        # to create the part, so we call super().__init__ here
        super().__init__(riser_params)


    def calculate_area(self) -> float:
        return self.part_params.riser_length * self.part_params.riser_height

    def calculate_volume(self) -> float:
        return self.calculate_area() * self.part_params.riser_thickness

    def _build(self) -> cq.Workplane:
        # Create a simple riser part
        return (
            cq.Workplane("YZ")
            .polyline([
                (0, 0),
                (0, inch_to_mm(self.part_params.riser_height)),
                (inch_to_mm(self.part_params.riser_thickness), inch_to_mm(self.part_params.riser_height)),
                (inch_to_mm(self.part_params.riser_thickness), 0)
            ])
            .close()
            .extrude(inch_to_mm(self.part_params.riser_length))
        )



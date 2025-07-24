

import cadquery as cq
from utils.math import inch_to_mm


from logger import part_logger
# part_logger.info("Loading Tread class from part.stairs.tread module")


from part.part import Part
from models.part.stairs.tread_params import TreadParams


class Tread(Part):
    def __init__(self, tread_params: TreadParams):
        part_logger.info(f"Creating Tread with params: {tread_params}")
        self.part_params = tread_params
        # _build is run by parent class Part and it uses self.part_params
        # to create the part, so we call super().__init__ here
        super().__init__(tread_params)


    def _build(self) -> cq.Workplane:
        # Create a simple tread part
        return (
            cq.Workplane("YZ")
            .polyline([
                (0, 0),
                (0, inch_to_mm(self.part_params.tread_thickness)),
                (inch_to_mm(self.part_params.tread_depth), inch_to_mm(self.part_params.tread_thickness)),
                (inch_to_mm(self.part_params.tread_depth), 0)
            ])
            .close()
            .extrude(inch_to_mm(self.part_params.tread_length))
        )

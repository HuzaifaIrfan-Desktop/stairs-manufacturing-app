

import cadquery as cq
from utils.math import inch_to_mm


from logger import part_logger
# part_logger.info("Loading Tread class from part.stairs.tread module")


from part.part import Part
from models.part.top_floor_opening_params import TopFloorOpeningParams


class TopFloorOpening(Part):
    def __init__(self, opening_params: TopFloorOpeningParams):
        part_logger.info(f"Creating TopFloorOpening with params: {opening_params}")
        self.part_params = opening_params
        # _build is run by parent class Part and it uses self.part_params
        # to create the part, so we call super().__init__ here
        super().__init__(opening_params)


    def _build(self) -> cq.Workplane:
        # Create a hollow rectangular opening in the XY plane
        outer = cq.Workplane("XY").rect(
            inch_to_mm(self.part_params.opening_width + 2 * self.part_params.opening_floor_outward_thickness),
            inch_to_mm(self.part_params.opening_length + 2 * self.part_params.opening_floor_outward_thickness)
        )
        inner = cq.Workplane("XY").rect(
            inch_to_mm(self.part_params.opening_width),
            inch_to_mm(self.part_params.opening_length)
        )
        cq_part = outer.extrude(inch_to_mm(self.part_params.opening_thickness)).cut(
                inner.extrude(inch_to_mm(self.part_params.opening_thickness))
        )

        # Position the opening based on the parameters
        cq_part = cq_part.translate(
            (
                inch_to_mm(self.part_params.opening_x_position + self.part_params.opening_width / 2),
                inch_to_mm(self.part_params.opening_y_position + self.part_params.opening_length / 2)
            )
        )


        # Position the opening at the top position
        cq_part = cq_part.translate((0, 0, inch_to_mm(self.part_params.opening_top_position - self.part_params.opening_thickness)))

        return cq_part

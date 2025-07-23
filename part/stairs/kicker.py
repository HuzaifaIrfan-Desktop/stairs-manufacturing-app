

import cadquery as cq
from utils.math import inch_to_mm

from logger import part_logger
# part_logger.info("Loading Kicker class from part.stairs.kicker module")

from part.part import Part
from models.part.stairs.kicker_params import KickerParams

class Kicker(Part):
    def __init__(self, kicker_params: KickerParams):
        part_logger.info(f"Creating Kicker with params: {kicker_params}")
        self.part_params = kicker_params
        # _build is run by parent class Part and it uses self.part_params
        # to create the part, so we call super().__init__ here
        super().__init__(kicker_params)


    def calculate_area(self) -> float:
        return self.part_params.kicker_length * self.part_params.kicker_height

    def calculate_volume(self) -> float:
        return self.calculate_area() * self.part_params.kicker_depth

    def _build(self) -> cq.Workplane:
        # Create a simple kicker part
        if not self.part_params.kicker_length or not self.part_params.kicker_height or not self.part_params.kicker_depth:
            part_logger.error("Kicker parameters are not set correctly.")
            return (
                cq.Workplane("YZ").polyline([
                    (0, 0),
                    (inch_to_mm(1), 0),
                    (inch_to_mm(1), inch_to_mm(1)),
                    (0, inch_to_mm(1))
                ])
            .close()
            .extrude(inch_to_mm(1))
            )
            # raise ValueError("Kicker parameters must be set before building the part.")
        return (
            cq.Workplane("YZ")
            .polyline([
                (0, 0),
                (inch_to_mm(self.part_params.kicker_depth), 0),
                (inch_to_mm(self.part_params.kicker_depth), inch_to_mm(self.part_params.kicker_height)),
                (0, inch_to_mm(self.part_params.kicker_height))
            ])
            .close()
            .extrude(inch_to_mm(self.part_params.kicker_length))
        )


    def export_drawing(self) -> str:
        file_path = self.export_dxf_right_view()

        self.export_drawing_from_dxf(file_path, text_scale=0.5)

        return file_path

        
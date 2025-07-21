

import cadquery as cq
from utils.math import inch_to_mm

from logger import part_logger
part_logger.info("Loading Kicker class from part.stairs.kicker module")
from drawings.dimensioned_dxf_exporter import DimensionedDXFExporter
from part.part import Part
from models.part.stairs.kicker_params import KickerParams

class Kicker(Part):
    def __init__(self, kicker_params: KickerParams):
        part_logger.info(f"Creating Kicker with params: {kicker_params}")
        self.kicker_params = kicker_params
        # _build is run by parent class Part and it uses self.kicker_params
        # to create the part, so we call super().__init__ here
        super().__init__(kicker_params)


    def calculate_area(self) -> float:
        return self.kicker_params.kicker_length * self.kicker_params.kicker_height

    def calculate_volume(self) -> float:
        return self.calculate_area() * self.kicker_params.kicker_depth

    def _build(self) -> cq.Workplane:
        # Create a simple kicker part
        return (
            cq.Workplane("YZ")
            .polyline([
                (0, 0),
                (inch_to_mm(self.kicker_params.kicker_depth), 0),
                (inch_to_mm(self.kicker_params.kicker_depth), inch_to_mm(self.kicker_params.kicker_height)),
                (0, inch_to_mm(self.kicker_params.kicker_height))
            ])
            .close()
            .extrude(inch_to_mm(self.kicker_params.kicker_length))
        )


    def export_dxf_right_view(self) -> str:
        file_path = super().export_dxf_right_view()

        DimensionedDXFExporter(file_path, text_scale=0.5).export()

        return file_path

        
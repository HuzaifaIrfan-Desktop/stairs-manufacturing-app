


import cadquery as cq
from utils.math import inch_to_mm


from logger import part_logger
# part_logger.info("Loading Tread class from part.stairs.tread module")


from part.part import Part
from models.part.landing.landing_params import LandingParams

class Landing(Part):
    def __init__(self, landing_params: LandingParams):
        part_logger.info(f"Creating Landing with params: {landing_params}")
        self.part_params = landing_params
        # _build is run by parent class Part and it uses self.part_params
        # to create the part, so we call super().__init__ here
        super().__init__(landing_params)


    def _build(self) -> cq.Workplane:
        # Create a hollow rectangular opening in the XY plane

        cq_part = cq.Workplane("XY").rect(
            inch_to_mm(self.part_params.landing_width),
            inch_to_mm(self.part_params.landing_length)
        ).extrude(inch_to_mm(self.part_params.landing_thickness))

        # Position the opening based on the parameters
        cq_part = cq_part.translate(
            (
                inch_to_mm(self.part_params.landing_x_position + self.part_params.landing_width / 2),
                inch_to_mm(self.part_params.landing_y_position + self.part_params.landing_length / 2)
            )
        )


        # Position the opening at the top position
        cq_part = cq_part.translate((0, 0, inch_to_mm(self.part_params.landing_top_position - self.part_params.landing_thickness)))

        return cq_part



    def export_drawings(self) -> str:
        dxf_file_path = self.export_dxf_top_view()

        drawing_pdf_file_path = self.export_drawing_from_dxf(dxf_file_path, text_scale=7.0)

        return drawing_pdf_file_path




import cadquery as cq
from utils.math import inch_to_mm

from drawing.drawing import Drawing
from utils.math import inch_to_mm

from logger import part_logger
# part_logger.info("Loading Tread class from part.stairs.tread module")


from part.part import Part
from models.part.landing.u_landing_params import ULandingParams

class ULanding(Part):
    def __init__(self, u_landing_params: ULandingParams):
        part_logger.info(f"Creating Landing with params: {u_landing_params}")
        self.part_params = u_landing_params
        # _build is run by parent class Part and it uses self.part_params
        # to create the part, so we call super().__init__ here
        super().__init__(u_landing_params)


    def _build(self) -> cq.Workplane:
        # Create a hollow rectangular opening in the XY plane

        points=[]

        current_x = 0
        current_y = self.part_params.landing_width
        points.append((inch_to_mm(current_x), inch_to_mm(current_y)))

        current_x = self.part_params.landing_length
        points.append((inch_to_mm(current_x), inch_to_mm(current_y)))



        if not self.part_params.right_hand_turn:
            # default left turn
            current_y -=  (self.part_params.landing_width)
            points.append((inch_to_mm(current_x), inch_to_mm(current_y)))
            current_x -= (self.part_params.landing_length - self.part_params.stairway_width)
            points.append((inch_to_mm(current_x), inch_to_mm(current_y)))
            current_y  -=  self.part_params.upper_stairway_placement_overhang
            points.append((inch_to_mm(current_x), inch_to_mm(current_y)))
        else:
            # right hand turn
            current_y -= (self.part_params.landing_width + self.part_params.upper_stairway_placement_overhang)
            points.append((inch_to_mm(current_x), inch_to_mm(current_y)))
            current_x -= self.part_params.stairway_width
            points.append((inch_to_mm(current_x), inch_to_mm(current_y)))
            current_y  +=  self.part_params.upper_stairway_placement_overhang
            points.append((inch_to_mm(current_x), inch_to_mm(current_y)))


        current_x = 0
        points.append((inch_to_mm(current_x), inch_to_mm(current_y)))


        cq_part=cq.Workplane("XY").polyline(points).close().extrude(inch_to_mm(self.part_params.landing_thickness))


        
        

        # Position the opening based on the parameters
        cq_part = cq_part.translate(
            (
                inch_to_mm(self.part_params.landing_x_position),
                inch_to_mm(self.part_params.landing_y_position)
            )
        )


        # Position the opening at the top position
        cq_part = cq_part.translate((0, 0, inch_to_mm(self.part_params.landing_top_position - self.part_params.landing_thickness)))

        return cq_part


    def export_drawing_from_dxf(self, dxf_file_path: str, text_scale: float = 1.0) -> str:
        center_text= f"{self.part_params.landing_top_position} (in) UP "
        drawing = Drawing(job_name=self.part_params.job_name, part_name=self.part_params.part_name, dxf_file_path=dxf_file_path, text_scale=text_scale, center_text=center_text)
        drawing_pdf_file_path = drawing.export()

        return drawing_pdf_file_path



    def export_drawing(self) -> str:
        dxf_file_path = self.export_dxf_top_view()

        drawing_pdf_file_path = self.export_drawing_from_dxf(dxf_file_path, text_scale=7.0)

        return drawing_pdf_file_path

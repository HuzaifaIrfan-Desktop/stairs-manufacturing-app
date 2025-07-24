

import cadquery as cq
from utils.math import inch_to_mm


from logger import part_logger
# part_logger.info("Loading SawtoothStringer class from part.stairs.sawtooth_stringer module")


from part.part import Part
from models.part.stairs.sawtooth_stringer_params import SawtoothStringerParams
import math


class SawtoothStringer(Part):
    def __init__(self, stringer_params: SawtoothStringerParams):
        part_logger.info(f"Creating SawtoothStringer with params: {stringer_params}")
        self.part_params = stringer_params
        # _build is run by parent class Part and it uses self.part_params
        # to create the part, so we call super().__init__ here
        super().__init__(stringer_params)


    def _build(self) -> cq.Workplane:
        # Create a simple sawtooth stringer part

        points = []

        first_x = inch_to_mm(self.part_params.bottom_stringer_placement_depth)
        first_y = 0


        current_x = first_x
        current_y = first_y
        points.append((current_x, current_y))

        if self.part_params.stringer_kicker_height > 0 and self.part_params.stringer_kicker_depth > 0:
            current_x+= -(inch_to_mm(self.part_params.bottom_stringer_placement_depth)-inch_to_mm(self.part_params.stringer_kicker_depth))
            points.append((current_x, current_y))
            current_y += inch_to_mm(self.part_params.stringer_kicker_height)
            points.append((current_x, current_y))

            current_x += -inch_to_mm(self.part_params.stringer_kicker_depth)
            points.append((current_x, current_y))
            current_y += (inch_to_mm(self.part_params.first_stringer_rise_height)-inch_to_mm(self.part_params.stringer_kicker_height))
            points.append((current_x, current_y))

        else:
            current_x += -inch_to_mm(self.part_params.bottom_stringer_placement_depth)
            points.append((current_x, current_y))
            current_y += inch_to_mm(self.part_params.first_stringer_rise_height)
            points.append((current_x, current_y))
        
        # one minus because the last run will be added after the loop
        for i in range(self.part_params.number_of_stringer_rise-1):
            current_x += inch_to_mm(self.part_params.typical_stringer_run_depth)
            points.append((current_x, current_y))
            current_y += inch_to_mm(self.part_params.typical_stringer_rise_height)
            points.append((current_x, current_y))

        current_x += inch_to_mm(self.part_params.last_stringer_run_depth)
        points.append((current_x, current_y))

        current_y -= inch_to_mm(self.part_params.back_stringer_hanger_height)
        points.append((current_x, current_y))

        stringer_part=(
            cq.Workplane("YZ").polyline(points).close().extrude(inch_to_mm(self.part_params.stringer_thickness))
        )
        return stringer_part
    


       
    def export_cam(self) -> str:

        cq_part = self.get()
        # Translate the stringer for rotation
        cq_part = cq_part.translate((0, -inch_to_mm(self.part_params.bottom_stringer_placement_depth), 0))
        cq_part = cq_part.rotate((0, 0, 0), (1, 0, 0), -math.degrees(self.part_params.angle_of_stringer_rad))
        reverse_translate_y = inch_to_mm(self.part_params.bottom_stringer_placement_depth * math.cos(self.part_params.angle_of_stringer_rad))
        cq_part = cq_part.translate((0, reverse_translate_y, 0))

        step_file_path = f'{self.part_output_dir}/CAM_{self.part_params.part_name}.step'
        # Export the part to a file STEP
        cq.exporters.export(cq_part, step_file_path, 'STEP')


        stl_file_path = f'{self.part_output_dir}/CAM_{self.part_params.part_name}.stl'
        # Export the part to a file STL
        cq.exporters.export(cq_part, stl_file_path, 'STL')


        dxf_file_path = f'{self.part_output_dir}/CAM_{self.part_params.part_name}_right.dxf'
        # Get a 2D projection for DXF
        right_view = cq_part.faces(">X").wires()
        cq.exporters.export(right_view, dxf_file_path, 'DXF')

        self.export_drawing_from_dxf(dxf_file_path, text_scale=7.0)

        return dxf_file_path
    
    def export_drawing(self) -> str:
        file_path = self.export_dxf_right_view()

        self.export_drawing_from_dxf(file_path, text_scale=7.0)

        return file_path

        
        
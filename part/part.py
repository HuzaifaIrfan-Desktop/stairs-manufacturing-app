import cadquery as cq
from utils.math import inch_to_mm

from models.part.part_params import PartParams

import os

class Part:
    def __init__(self, part_params: PartParams):
        # print(f"Creating Part with params: {part_params}")
        self.part_params = part_params

        self.part_output_dir = os.path.join(os.getcwd(), f'output/{self.part_params.job_name}/part/')
        
        # Ensure the output directory exists
        os.makedirs(self.part_output_dir, exist_ok=True)

        self.cq_part = self._build()

    def _build(self) -> cq.Workplane:
        # Create a simple part based on the parameters
        return (
            cq.Workplane("XY")
            .box(inch_to_mm(1), inch_to_mm(1), inch_to_mm(1))  # Placeholder dimensions
        )


    def get(self) -> cq.Workplane:
        return self.cq_part
    
    def export_step(self) -> str:
        file_path = f'{self.part_output_dir}/{self.part_params.part_name}.step'
        # Export the part to a file STEP
        cq.exporters.export(self.cq_part, file_path, 'STEP')
        return file_path


    def export_stl(self) -> str:
        file_path = f'{self.part_output_dir}/{self.part_params.part_name}.stl'
        # Export the part to a file STL
        cq.exporters.export(self.cq_part, file_path, 'STL')
        return file_path

    def export_dxf_top_view(self) -> str:
        file_path = f'{self.part_output_dir}/{self.part_params.part_name}_top.dxf'
        # Get a 2D projection for DXF
        top_view = self.cq_part.faces(">Z").wires()
        cq.exporters.export(top_view, file_path, 'DXF')
        return file_path

    def export_dxf_front_view(self) -> str:
        file_path = f'{self.part_output_dir}/{self.part_params.part_name}_front.dxf'
        # Get a 2D projection for DXF
        front_view = self.cq_part.faces(">Y").wires()
        cq.exporters.export(front_view, file_path, 'DXF')
        return file_path

    def export_dxf_right_view(self) -> str:
        file_path = f'{self.part_output_dir}/{self.part_params.part_name}_right.dxf'
        # Get a 2D projection for DXF
        right_view = self.cq_part.faces(">X").wires()
        cq.exporters.export(right_view, file_path, 'DXF')
        return file_path

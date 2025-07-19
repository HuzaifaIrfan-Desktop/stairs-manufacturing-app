

import cadquery as cq
import os
from models.part.stairs.tread_params import TreadParams


from utils.math import inch_to_mm


class Tread:
    def __init__(self, tread_params: TreadParams):
        self.tread_params = tread_params
        self.cq_part = self._build()
        self.output_dir = f'output/{self.tread_params.job_name}/part/stairs/'
        # Ensure the output directory exists
        
        os.makedirs(self.output_dir, exist_ok=True)

    def calculate_area(self) -> float:
        return self.tread_params.tread_length * self.tread_params.tread_depth

    def calculate_volume(self) -> float:
        return self.calculate_area() * self.tread_params.tread_thickness

    def _build(self) -> cq.Workplane:
        # Create a simple tread part
        return (
            cq.Workplane("XY")
            .box(inch_to_mm(self.tread_params.tread_length), inch_to_mm(self.tread_params.tread_depth), inch_to_mm(self.tread_params.tread_thickness))
        )

    def get(self) -> cq.Workplane:
        return self.cq_part
    
    def _export_step(self) -> None:
        file_path = f'{self.output_dir}/tread_{self.tread_params.part_name}.step'
        # Export the part to a file STEP
        cq.exporters.export(self.cq_part, file_path, 'STEP')

    
    def _export_stl(self) -> None:
        file_path = f'{self.output_dir}/tread_{self.tread_params.part_name}.stl'
        # Export the part to a file STL
        cq.exporters.export(self.cq_part, file_path, 'STL')

    def _export_dxf(self) -> None:
        file_path = f'{self.output_dir}/tread_{self.tread_params.part_name}.dxf'
        # Get a 2D projection for DXF
        top_view = self.cq_part.faces(">Z").wires()
        cq.exporters.export(top_view, file_path, 'DXF')

    def export_all(self) -> None:
        self._export_step()
        self._export_stl()
        self._export_dxf()
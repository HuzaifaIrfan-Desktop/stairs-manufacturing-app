import cadquery as cq

from drawing.drawing import Drawing
from utils.math import inch_to_mm

from logger import part_logger
# part_logger.info("Loading Part class from part.part module")


from models.part.part_params import PartParams

import os

class Part:
    def __init__(self, part_params: PartParams):
        # part_logger.info(f"Creating Part with params: {part_params}")
        self.part_params = part_params

        self.part_output_dir = os.path.join(os.getcwd(), f'output/{self.part_params.job_name}/part/{self.part_params.part_name}')
        
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
    
    def get_part_params(self) -> PartParams:
        return self.part_params
    
    def export(self) -> str:
        self.export_part_params()

        stl_file_path = self.export_stl()
        self.export_step()
        self.export_dxf_top_view()
        self.export_dxf_front_view()
        self.export_dxf_right_view()
        
        self.export_drawing()

        return stl_file_path

    def export_part_params(self) -> str:
        # Export the part parameters to a file
        json_file_path = f'{self.part_output_dir}/{self.part_params.part_name}_params.json'
        with open(json_file_path, 'w') as f:
            f.write(self.part_params.model_dump_json(indent=4))
        return json_file_path
    
    def export_step(self) -> str:
        step_file_path = f'{self.part_output_dir}/{self.part_params.part_name}.step'
        # Export the part to a file STEP
        cq.exporters.export(self.cq_part, step_file_path, 'STEP')
        return step_file_path


    def export_stl(self) -> str:
        stl_file_path = f'{self.part_output_dir}/{self.part_params.part_name}.stl'
        # Export the part to a file STL
        cq.exporters.export(self.cq_part, stl_file_path, 'STL')
        return stl_file_path

    def export_dxf_top_view(self) -> str:
        dxf_file_path = f'{self.part_output_dir}/{self.part_params.part_name}_top.dxf'
        # Get a 2D projection for DXF
        top_view = self.cq_part.faces(">Z").wires()
        cq.exporters.export(top_view, dxf_file_path, 'DXF')
        return dxf_file_path

    def export_dxf_front_view(self) -> str:
        dxf_file_path = f'{self.part_output_dir}/{self.part_params.part_name}_front.dxf'
        # Get a 2D projection for DXF
        front_view = self.cq_part.faces(">Y").wires()
        cq.exporters.export(front_view, dxf_file_path, 'DXF')
        return dxf_file_path

    def export_dxf_right_view(self) -> str:
        dxf_file_path = f'{self.part_output_dir}/{self.part_params.part_name}_right.dxf'
        # Get a 2D projection for DXF
        right_view = self.cq_part.faces(">X").wires()
        cq.exporters.export(right_view, dxf_file_path, 'DXF')
        
        return dxf_file_path


    def export_drawing_from_dxf(self, dxf_file_path: str, text_scale: float = 1.0) -> str:
        drawing = Drawing(job_name=self.part_params.job_name, part_name=self.part_params.part_name, dxf_file_path=dxf_file_path, text_scale=text_scale)
        drawing_pdf_file_path = drawing.export()

        return drawing_pdf_file_path


    def export_drawing(self) -> str:
        dxf_file_path = self.export_dxf_right_view()

        drawing_pdf_file_path = self.export_drawing_from_dxf(dxf_file_path, text_scale=1.0)

        return drawing_pdf_file_path


import cadquery as cq
from drawing.drawing import Drawing
from utils.math import inch_to_mm

from models.assembly.assembly_params import AssemblyParams

from models.report.cut_list_params import CutListParams
from report.cut_list_report import CutListReport    

from logger import assembly_logger

import os
class Assembly:
    def __init__(self, assembly_params: AssemblyParams):
        self.assembly_params = assembly_params

        self.assembly_output_dir = os.path.join(os.getcwd(), f'output/{self.assembly_params.job_name}/assembly/{self.assembly_params.assembly_name}')
        
        # Ensure the output directory exists
        os.makedirs(self.assembly_output_dir, exist_ok=True)

        self._build()
        self._assemble()

        assembly_logger.info(f"Initialized Assembly with job_name: {self.assembly_params.job_name}, assembly_name: {self.assembly_params.assembly_name}")

    def _build(self):
        pass


    def _assemble(self):
        box1 = cq.Workplane("XY").box(10, 10, 10).val()
        box2 = cq.Workplane("XY").box(10, 10, 10).val().translate((15, 0, 0))  # offset after creation

        compound = cq.Compound.makeCompound([box1, box2])
        self.cq_assembly = cq.Workplane(obj=compound)

    def get(self) -> cq.Workplane:
        return self.cq_assembly

    def get_assembly_params(self) -> AssemblyParams:
        return self.assembly_params
    
    def export(self) -> str:
        self.export_assembly_params()

        stl_file_path = self.export_stl()
        self.export_step()
        self.export_dxf_top_view()
        self.export_dxf_front_view()
        self.export_dxf_right_view()
        
        # self.export_drawing()

        self.export_cut_list()

        self.export_parts()
        
        self.export_drawing()

        return stl_file_path

    def export_assembly_params(self) -> str:
        # Export the assembly parameters to a file
        file_path = f'{self.assembly_output_dir}/{self.assembly_params.assembly_name}_params.json'
        with open(file_path, 'w') as f:
            f.write(self.assembly_params.model_dump_json(indent=4))
        return file_path
    
    def export_step(self) -> str:
        file_path = f'{self.assembly_output_dir}/{self.assembly_params.assembly_name}.step'
        # Export the part to a file STEP
        cq.exporters.export(self.cq_assembly, file_path, 'STEP')
        return file_path


    def export_stl(self) -> str:
        file_path = f'{self.assembly_output_dir}/{self.assembly_params.assembly_name}.stl'
        # Export the part to a file STL
        cq.exporters.export(self.cq_assembly, file_path, 'STL')
        return file_path

    def export_dxf_top_view(self) -> str:
        file_path = f'{self.assembly_output_dir}/{self.assembly_params.assembly_name}_top.dxf'
        # Get a 2D projection for DXF
        top_view = self.cq_assembly.faces(">Z").wires()
        cq.exporters.export(top_view, file_path, 'DXF')
        return file_path

    def export_dxf_front_view(self) -> str:
        file_path = f'{self.assembly_output_dir}/{self.assembly_params.assembly_name}_front.dxf'
        # Get a 2D projection for DXF
        front_view = self.cq_assembly.faces(">Y").wires()
        cq.exporters.export(front_view, file_path, 'DXF')
        return file_path

    def export_dxf_right_view(self) -> str:
        file_path = f'{self.assembly_output_dir}/{self.assembly_params.assembly_name}_right.dxf'
        
        # Get a 2D projection for DXF
        right_wires = self.cq_assembly.faces("-X").wires()

        # --- Step 3: Flatten wires onto YZ plane as sketch is drawn on YZ for DXF ---
        flattened = cq.Workplane("YZ").add(right_wires)

        # --- Step 4: Export to DXF ---
        cq.exporters.export(flattened, file_path, 'DXF')
        return file_path

    def export_cut_list(self) -> str:


        cut_list_params = CutListParams(
            job_name=self.assembly_params.job_name,
            assembly_name=self.assembly_params.assembly_name,
            builder_name=self.assembly_params.builder_name,
            summary_items=[("Item", "Description")],
            cut_list_data=[["Box1", "10x10x10"], ["Box2", "10x10x10"]]
        )

        cut_list_report = CutListReport(cut_list_params)
        file_path = cut_list_report.export()

        return file_path


    def export_drawing_from_dxf(self, dxf_file_path: str, text_scale: float = 1.0) -> str:
        drawing = Drawing(job_name=self.assembly_params.job_name, part_name=self.assembly_params.assembly_name, dxf_file_path=dxf_file_path, text_scale=text_scale)
        drawing_pdf_file_path = drawing.export()

        return drawing_pdf_file_path


    def export_drawing(self) -> str:
        # Placeholder for drawing export logic
        file_path = ""

        return file_path

    def export_parts(self) -> str:
        file_path=""

        return file_path
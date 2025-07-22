
import cadquery as cq
from utils.math import inch_to_mm

from models.assembly.assembly_params import AssemblyParams

import os
class Assembly:
    def __init__(self, assembly_params: AssemblyParams):
        self.assembly_params = assembly_params

        self.assembly_output_dir = os.path.join(os.getcwd(), f'output/{self.assembly_params.job_name}/assembly/{self.assembly_params.assembly_name}')
        
        # Ensure the output directory exists
        os.makedirs(self.assembly_output_dir, exist_ok=True)

        self._build()
        self._assemble()

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
        right_view = self.cq_assembly.faces(">X").wires()
        cq.exporters.export(right_view, file_path, 'DXF')
        return file_path

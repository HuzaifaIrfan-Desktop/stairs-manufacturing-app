

import os
from models.job.job_params import JobInputParams
import cadquery as cq
from utils.math import inch_to_mm


class Job:
    def __init__(self, job_input_params: JobInputParams):
        self.job_input_params = job_input_params
        self.output_dir = os.path.join(os.getcwd(), 'output', self.job_input_params.job_name)
        os.makedirs(self.output_dir, exist_ok=True)

        if not self.job_output_params:
            self.job_output_params = JobInputParams()

        self._build()
        self._assemble()


    def _build(self):
        pass


    def _assemble(self):
        box1 = cq.Workplane("XY").box(10, 10, 10).val()
        box2 = cq.Workplane("XY").box(10, 10, 10).val().translate((15, 0, 0))  # offset after creation

        compound = cq.Compound.makeCompound([box1, box2])
        self.cq_job_assembly = cq.Workplane(obj=compound)

    def get(self) -> cq.Workplane:
        return self.cq_job_assembly

    def get_job_input_params(self) -> JobInputParams:
        return self.job_input_params

    def get_job_output_params(self) -> JobInputParams:
        return self.job_output_params

    def export_job_params(self) -> str:
        # Export the job parameters to a file
        job_input_params_file_path = f'{self.output_dir}/{self.job_input_params.job_name}_params.json'
        with open(job_input_params_file_path, 'w') as f:
            f.write(self.job_input_params.model_dump_json(indent=4))

        job_output_params_file_path = f'{self.output_dir}/{self.job_input_params.job_name}_output.json'
        with open(job_output_params_file_path, 'w') as f:
            f.write(self.job_output_params.model_dump_json(indent=4))

        return job_input_params_file_path


    def export_step(self) -> str:
        file_path = f'{self.output_dir}/{self.job_input_params.job_name}.step'
        # Export the part to a file STEP
        cq.exporters.export(self.cq_job_assembly, file_path, 'STEP')
        return file_path


    def export_stl(self) -> str:
        file_path = f'{self.output_dir}/{self.job_input_params.job_name}.stl'
        # Export the part to a file STL
        cq.exporters.export(self.cq_job_assembly, file_path, 'STL')
        return file_path

    def export_dxf_top_view(self) -> str:
        file_path = f'{self.output_dir}/{self.job_input_params.job_name}_top.dxf'
        # Get a 2D projection for DXF
        top_view = self.cq_job_assembly.faces(">Z").wires()
        cq.exporters.export(top_view, file_path, 'DXF')
        return file_path

    def export_dxf_front_view(self) -> str:
        file_path = f'{self.output_dir}/{self.job_input_params.job_name}_front.dxf'
        # Get a 2D projection for DXF
        front_view = self.cq_job_assembly.faces(">Y").wires()
        cq.exporters.export(front_view, file_path, 'DXF')
        return file_path

    def export_dxf_right_view(self) -> str:
        file_path = f'{self.output_dir}/{self.job_input_params.job_name}_right.dxf'
        # Get a 2D projection for DXF
        right_view = self.cq_job_assembly.faces(">X").wires()
        cq.exporters.export(right_view, file_path, 'DXF')
        return file_path

    def export(self) -> str:
        # Export the job parameters to a file
        file_path = self.export_job_params()
        return file_path
    

    def export_assembly(self) -> str:
        # Export the assembly to a file
        file_path = self.export_stl()
        return file_path
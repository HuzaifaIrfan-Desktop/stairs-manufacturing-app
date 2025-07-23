

import os
from models.job.job_params import JobInputParams

class Job:
    def __init__(self, job_input_params: JobInputParams):
        self.job_input_params = job_input_params
        self.output_dir = f'output/{self.job_input_params.job_name}'
        os.makedirs(self.output_dir, exist_ok=True)


    def export_job_params(self) -> str:
        # Export the job parameters to a file
        file_path = f'{self.output_dir}/{self.job_input_params.job_name}_params.json'
        with open(file_path, 'w') as f:
            f.write(self.job_input_params.model_dump_json(indent=4))
        return file_path


    def export(self) -> str:
        # Export the job parameters to a file
        file_path = self.export_job_params()
        return file_path
    

    def export_assembly(self) -> str:
        # Export the assembly to a file
        file_path = ""
        return file_path
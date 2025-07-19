

from models.job.job_input_params import JobInputParams

class Job:
    def __init__(self, job_input_params: JobInputParams):
        self.job_input_params = job_input_params
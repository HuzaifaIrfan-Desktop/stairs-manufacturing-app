

from models.job.job_params import JobInputParams

class Job:
    def __init__(self, job_input_params: JobInputParams):
        self.job_input_params = job_input_params
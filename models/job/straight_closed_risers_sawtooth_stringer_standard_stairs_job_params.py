

from models.job.job_params import JobInputParams

class StraightClosedRisersSawtoothStringerStandardStairsJobInputParams(JobInputParams):
    riser_height: float = 0.18
    tread_depth: float = 0.30
    stringer_length: float = 3.0
    number_of_steps: int = 12

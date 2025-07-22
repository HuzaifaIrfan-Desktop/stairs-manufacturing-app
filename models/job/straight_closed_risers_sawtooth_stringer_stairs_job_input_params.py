

from models.job.job_params import JobInputParams

class StraightClosedRisersSawtoothStringerStairsJobInputParams(JobInputParams):
    riser_height: float
    tread_depth: float
    stringer_length: float
    number_of_steps: int

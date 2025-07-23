

from models.job.job_params import JobInputParams

class StraightClosedRisersSawtoothStringerStandardStairsJobInputParams(JobInputParams):
    riser_height: float = 0.18
    tread_depth: float = 0.30
    stringer_length: float = 3.0
    number_of_steps: int = 12
    number_of_stringers: int = 2
    has_nosing: bool = True
    nosing_depth: float = 0.025 
    has_risers: bool = True
    riser_thickness: float = 0.02
    has_stringers: bool = True
    stringer_thickness: float = 0.02
    has_open_riser: bool = False
    



from models.job.job_input_params import JobInputParams

class StraightClosedRisersSawtoothStringerStairsJobInputParams(JobInputParams):
    riser_height: float
    tread_depth: float
    stringer_length: float
    number_of_steps: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        use_enum_values = True
        extra = "forbid"
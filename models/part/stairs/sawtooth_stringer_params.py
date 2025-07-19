
from models.part.part_params import PartParams

class SawtoothStringerParams(PartParams):
    
    stringer_width: float
    stringer_thickness: float

    stringer_length: float

    first_step_rise_height: float
    last_step_run_depth: float

    step_rise_height: float
    step_run_depth: float

    number_of_stringer_rise: int
    number_of_stringer_run: int

    angle_of_stringer: float
    stringer_placement_from_top: float
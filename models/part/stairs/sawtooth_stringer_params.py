
from models.part.part_params import PartParams

import math

import math

def calculate_stringer_bounds(rise, run, width):
    """
    Calculate the x and y offsets from the sawtooth start/end to the bounding stringer.
    
    Args:
        rise (float): The vertical rise of one step.
        run (float): The horizontal run of one step.
        width (float): The perpendicular distance from the sawtooth corner to the stringer edge.
    
    Returns:
        (x, y): Tuple of floats representing the horizontal and vertical offsets.
    """
    # The angle of the stringer (hypotenuse)
    angle_rad = math.atan2(rise, run)

    # x = width * cos(angle_rad)
    # y = width * sin(angle_rad)
    x = width * math.cos(angle_rad)
    y = width * math.sin(angle_rad)

    return x, y


class SawtoothStringerParams(PartParams):
    
    stringer_width: float
    stringer_thickness: float

    stringer_length: float

    first_step_rise_height: float
    last_step_run_depth: float

    step_rise_height: float
    step_run_depth: float

    number_of_stringer_rise: int # Same as run and not used in calculations
    number_of_stringer_run: int # This is the number of runs, not the number of treads

    angle_of_stringer: float
    stringer_placement_from_top: float

    bottom_stringer_depth: float = None
    back_stringer_reverse_height: float = None

    kicker_height: float = 0.0
    kicker_depth: float = 0.0




    def __init__(self, **data):
        super().__init__(**data)
        if self.bottom_stringer_depth is None or self.back_stringer_reverse_height is None:
            self.bottom_stringer_depth, self.back_stringer_reverse_height = calculate_stringer_bounds(
                self.step_rise_height,
                self.step_run_depth,
                self.stringer_width
            )



    def __post_init__(self):
        if self.kicker_height >= self.first_step_rise_height:
            raise ValueError("kicker_height must be less than first_step_rise_height")
        if self.kicker_depth >= self.bottom_stringer_depth:
            raise ValueError("kicker_depth must be less than bottom_stringer_depth")
   
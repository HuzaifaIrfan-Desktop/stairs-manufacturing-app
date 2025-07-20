
from models.part.part_params import PartParams

import math

import math

def calculate_stringer_bounds(                first_step_rise_height: float,
                last_step_run_depth: float,
                step_rise_height: float,
                step_run_depth: float,
                number_of_stringer_run: int,
                stringer_width: float) -> tuple:
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
    angle_rad = math.atan2(step_rise_height, step_run_depth)


    def calculate_x(theta1_rad, w, r_f):
        """
        Calculate X using the formula:
        X = (w * sqrt(1 + tan^2(theta1)) - r_f) / tan(theta1)

        Parameters:
            theta1_rad (float): Angle θ₁ in radians
            w (float): Width
            r_f (float): r_f value (e.g., first rise or offset)

        Returns:
            float: Resulting X value
        """
        tan_theta1 = math.tan(theta1_rad)
        sqrt_term = math.sqrt(1 + tan_theta1**2)
        numerator = w * sqrt_term - r_f
        x = numerator / tan_theta1
        return x


    def calculate_y(theta1_rad, r_f, n, r_i, r_l, X):
        """
        Calculate Y using the formula:
        Y = r_f + n * r_i - tan(theta1) * ((n * r_i / tan(theta1)) + r_l - X)

        Parameters:
            theta1_rad (float): Angle θ₁ in radians
            r_f (float): First rise
            n (int): Number of risers
            r_i (float): Intermediate rise
            r_l (float): Last rise
            X (float): Previously calculated X value

        Returns:
            float: Resulting Y value
        """
        tan_theta1 = math.tan(theta1_rad)
        term_inside = (n * r_i / tan_theta1) + r_l - X
        Y = r_f + n * r_i - tan_theta1 * term_inside
        return Y

    x = calculate_x(angle_rad, stringer_width, first_step_rise_height)
    y = calculate_y(angle_rad, first_step_rise_height, 0, step_rise_height, last_step_run_depth, x)

    bottom_stringer_depth=x
    back_stringer_reverse_height=y


    def calculate_w_min(theta1_rad, r_u, r_f, X):
        """
        Calculate minimum width (w_min) using the formula:
        w_min = |tan(theta1) * r_u - r_f - tan(theta1) * X| / sqrt(tan^2(theta1) + 1)

        Parameters:
            theta1_rad (float): Angle θ₁ in radians
            r_u (float): Upper rise
            r_f (float): First rise
            X (float): Horizontal X value

        Returns:
            float: Minimum width (w_min)
        """
        tan_theta1 = math.tan(theta1_rad)
        numerator = abs(tan_theta1 * r_u - r_f - tan_theta1 * X)
        denominator = math.sqrt(tan_theta1**2 + 1)
        w_min = numerator / denominator
        return w_min

    w_min = calculate_w_min(angle_rad, step_run_depth, first_step_rise_height, x)

    return bottom_stringer_depth, back_stringer_reverse_height, w_min


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
    stringer_width_min: float = None  # Minimum width of the stringer based on calculations

    kicker_height: float = 0.0
    kicker_depth: float = 0.0




    def __init__(self, **data):
        super().__init__(**data)
        if self.bottom_stringer_depth is None or self.back_stringer_reverse_height is None:
            bottom_stringer_depth, back_stringer_reverse_height, w_min = calculate_stringer_bounds(
                self.first_step_rise_height,
                self.last_step_run_depth,
                self.step_rise_height,
                self.step_run_depth,
                self.number_of_stringer_run,
                self.stringer_width
            )
            self.bottom_stringer_depth = bottom_stringer_depth
            self.back_stringer_reverse_height = back_stringer_reverse_height
            self.stringer_width_min = w_min



    def __post_init__(self):
        if self.kicker_height >= self.first_step_rise_height:
            raise ValueError("kicker_height must be less than first_step_rise_height")
        if self.kicker_depth >= self.bottom_stringer_depth:
            raise ValueError("kicker_depth must be less than bottom_stringer_depth")
   
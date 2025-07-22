
from models.part.part_params import PartParams

import math
from models.material.lumber import Lumber,lumber_2x12

from pydantic import BaseModel, Field, model_validator


class SawtoothStringerParams(PartParams):
    stringer_width: float = Field(init=False, default=None, validate_default=False)
    stringer_thickness: float = Field(init=False, default=None, validate_default=False)

    stringer_length: float = Field(init=False, default=None, validate_default=False)

    stringer_total_rise: float = Field(init=False, default=None, validate_default=False)
    stringer_total_run: float = Field(init=False, default=None, validate_default=False)

    first_step_rise_height: float
    last_step_run_depth: float

    step_rise_height: float
    step_run_depth: float

    # number_of_stringer_rise: int = Field(init=False, default=None, validate_default=False) # Same as run and not used in calculations
    number_of_stringer_run: int # This is the number of runs, not the number of treads

    angle_of_stringer_rad: float = Field(init=False, default=None, validate_default=False)

    # init False should not be set externally; it's computed on initialization

    bottom_stringer_depth: float  = Field(init=False, default=None, validate_default=False)
    back_stringer_reverse_height: float = Field(init=False, default=None, validate_default=False)
    stringer_width_min: float = Field(init=False, default=None, validate_default=False)

    kicker_height: float = Field(default=0.0)
    kicker_depth: float = Field(default=0.0)

    material: Lumber = Field(default=lumber_2x12, description="Material of the stringer, e.g., Lumber, etc.")


    @model_validator(mode='after')
    def compute_bounds(self) -> 'SawtoothStringerParams':


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


        # stringer width and thickness from material
        self.stringer_width = self.material.width
        self.stringer_thickness = self.material.thickness


        # The angle of the stringer (hypotenuse)
        self.angle_of_stringer_rad = math.atan2(self.step_rise_height, self.step_run_depth)


        number_of_stringer_rise = self.number_of_stringer_run

        self.stringer_total_rise = self.first_step_rise_height + (number_of_stringer_rise - 1) * self.step_rise_height

        self.stringer_total_run  = self.last_step_run_depth + (self.number_of_stringer_run - 1) * self.step_run_depth

        self.stringer_length = math.sqrt(self.stringer_total_rise**2 + self.stringer_total_run**2)

        self.bottom_stringer_depth = calculate_x(self.angle_of_stringer_rad, self.stringer_width, self.first_step_rise_height)
        self.back_stringer_reverse_height = calculate_y(self.angle_of_stringer_rad, self.first_step_rise_height, 0, self.step_rise_height, self.last_step_run_depth, self.bottom_stringer_depth)

        self.stringer_width_min = calculate_w_min(self.angle_of_stringer_rad, self.step_run_depth, self.first_step_rise_height, self.bottom_stringer_depth)
        
        
        if self.kicker_height >= self.first_step_rise_height:
            raise ValueError("kicker_height must be less than first_step_rise_height")
        if self.kicker_depth >= self.bottom_stringer_depth:
            raise ValueError("kicker_depth must be less than bottom_stringer_depth")

        return self

    # def __init__(self, **data):
    #     super().__init__(**data)




   
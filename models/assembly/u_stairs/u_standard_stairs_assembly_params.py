

from pydantic import BaseModel, Field, model_validator

from models.assembly.assembly_params import AssemblyParams
from models.assembly.stairs.sawtooth_stringer.straight_sawtooth_stringer_standard_stairs_assembly_params import StraightSawtoothStringerStandardStairsAssemblyParams

from models.part.stairs.kicker_params import KickerParams
from models.part.stairs.sawtooth_stringer_params import SawtoothStringerParams
from models.part.stairs.riser_params import RiserParams
from models.part.stairs.tread_params import TreadParams

from models.part.landing.u_landing_params import ULandingParams



from models.material.material import Material
from models.material.lumber import Lumber, lumber_2x12, lsl_2x12
from models.material.plywood import Plywood, plywood_3_8, plywood_5_8, plywood_1

from typing import Union as union

class UStandardStairsAssemblyParams(AssemblyParams):

    total_rise_height: float = Field(description="Total rise height")
    opening_length: float = Field(description="Length of the opening")
    opening_width: float = Field(description="Width of the opening")


    center_wall_thickness: float = Field(default=0.0, description="Thickness of the center wall")



    number_of_upper_steps: int = Field(description="Number of steps")
    number_of_lower_steps: int = Field(description="Number of steps")
    stairway_width: float = Field(init=False, default=None, validate_default=False, description="Width of the stairway")


    u_landing_params: ULandingParams = Field(init=False, default=None, validate_default=False, description="Parameters for the landing")
    upper_standard_stairs_assembly_params: StraightSawtoothStringerStandardStairsAssemblyParams = Field(init=False, default=None, validate_default=False, description="Parameters for the sawtooth stringer")
    lower_standard_stairs_assembly_params: StraightSawtoothStringerStandardStairsAssemblyParams = Field(init=False, default=None, validate_default=False, description="Parameters for the sawtooth stringer")



    @model_validator(mode='after')
    def compute(self) -> 'UStandardStairsAssemblyParams':

        total_number_of_steps = self.number_of_upper_steps + self.number_of_lower_steps


        self.stairway_width = (self.opening_length - self.center_wall_thickness)/2

        





        self.u_landing_params = ULandingParams(
            job_name=self.job_name,
            part_name="u_landing",
            landing_top_position=0,
            landing_width=10,
            stairway_width=self.stairway_width,
            landing_length=self.opening_width
        )



        return self



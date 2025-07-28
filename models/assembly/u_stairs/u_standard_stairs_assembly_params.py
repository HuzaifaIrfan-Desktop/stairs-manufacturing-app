

import math
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

    total_opening_rise_height: float = Field( description="Total opening rise height")

    opening_length: float = Field(description="Length of the opening")
    opening_width: float = Field(description="Width of the opening")


    center_wall_thickness: float = Field(default=0.0, description="Thickness of the center wall")



    number_of_upper_steps: int = Field(description="Number of steps")
    number_of_lower_steps: int = Field(description="Number of steps")
    stairway_width: float = Field(init=False, default=None, validate_default=False, description="Width of the stairway")
    tread_depth: float = Field( description="Depth of the tread")


    open_riser: bool = Field(default=False, description="Open Riser")
    last_riser_hanger_height: float = Field(default=13.25, description="Height of the last riser hanger")


    u_landing_params: ULandingParams = Field(init=False, default=None, validate_default=False, description="Parameters for the landing")
    upper_standard_stairs_assembly_params: StraightSawtoothStringerStandardStairsAssemblyParams = Field(init=False, default=None, validate_default=False, description="Parameters for the sawtooth stringer")
    lower_standard_stairs_assembly_params: StraightSawtoothStringerStandardStairsAssemblyParams = Field(init=False, default=None, validate_default=False, description="Parameters for the sawtooth stringer")


    tread_overhang_nosing_depth: float = Field(default=0.0, description="Tread overhang nosing depth")
    tread_overhang_side_depth: float = Field(default=0.0, description="Tread overhang side depth")

    tread_material: Plywood = Field(default=plywood_1, description="Material of the tread, e.g., Plywood, etc.")
    riser_material: Plywood = Field(default=plywood_3_8, description="Material of the riser, e.g., Plywood, etc.")
    last_riser_hanger_material: Plywood = Field(default=plywood_5_8, description="Material of the last riser hanger, e.g., Plywood, etc.")
    stringer_material: Lumber = Field(default=lsl_2x12, description="Material of the stringer, e.g., Lumber, etc.")

    number_of_stringers: int = Field(default=2, description="Number of stringers")

    @model_validator(mode='after')
    def compute(self) -> 'UStandardStairsAssemblyParams':

        total_number_of_steps = self.number_of_upper_steps + self.number_of_lower_steps

        typical_riser_height: float = self.total_opening_rise_height / total_number_of_steps

        if typical_riser_height >= 7.875:
            minimum_number_of_steps = math.ceil(self.total_opening_rise_height / 7.875)
            raise ValueError("Maximum allowed riser height is 7.875 inches. Please adjust the number of steps. Minimum number of steps required is: {}".format(minimum_number_of_steps))
       
      

        upper_rise_height = self.total_opening_rise_height * (self.number_of_upper_steps / total_number_of_steps)
        lower_rise_height = self.total_opening_rise_height * (self.number_of_lower_steps / total_number_of_steps)

        self.stairway_width = (self.opening_width - self.center_wall_thickness)/2

        landing_top_position = lower_rise_height
    
        

        self.upper_standard_stairs_assembly_params = StraightSawtoothStringerStandardStairsAssemblyParams(
            job_name=self.job_name,
            assembly_name="upper_standard_stairs",
            builder_name=self.builder_name,
            total_opening_rise_height=upper_rise_height,
            number_of_steps=self.number_of_upper_steps,
            last_riser_hanger_height=self.last_riser_hanger_height,
            stairway_width=self.stairway_width,
            tread_depth=self.tread_depth,
            open_riser=self.open_riser,
            tread_overhang_nosing_depth=self.tread_overhang_nosing_depth,
            tread_overhang_side_depth=self.tread_overhang_side_depth,
            tread_material=self.tread_material,
            riser_material=self.riser_material,
            last_riser_hanger_material=self.last_riser_hanger_material,
            stringer_material=self.stringer_material,
            number_of_stringers=self.number_of_stringers
        )

        self.lower_standard_stairs_assembly_params = StraightSawtoothStringerStandardStairsAssemblyParams(
            job_name=self.job_name,
            assembly_name="lower_standard_stairs",
            builder_name=self.builder_name,
            total_opening_rise_height=lower_rise_height,
            number_of_steps=self.number_of_lower_steps,
            last_riser_hanger_height=self.last_riser_hanger_height,
            stairway_width=self.stairway_width,
            tread_depth=self.tread_depth,
            open_riser=self.open_riser,
            tread_overhang_nosing_depth=self.tread_overhang_nosing_depth,
            tread_overhang_side_depth=self.tread_overhang_side_depth,
            tread_material=self.tread_material,
            riser_material=self.riser_material,
            last_riser_hanger_material=self.last_riser_hanger_material,
            stringer_material=self.stringer_material,
            number_of_stringers=self.number_of_stringers
        )


        landing_width= self.opening_length - self.upper_standard_stairs_assembly_params.total_assembly_run_depth



        self.u_landing_params = ULandingParams(
            job_name=self.job_name,
            part_name="u_landing",
            landing_top_position=landing_top_position,
            landing_width=landing_width,
            stairway_width=self.stairway_width,
            landing_length=self.opening_width,
            landing_y_position=self.upper_standard_stairs_assembly_params.total_assembly_run_depth
        )



        return self



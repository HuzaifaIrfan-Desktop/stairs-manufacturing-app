

import math
from pydantic import BaseModel, Field, model_validator

from models.assembly.assembly_params import AssemblyParams

from models.part.stairs.kicker_params import KickerParams
from models.part.stairs.sawtooth_stringer_params import SawtoothStringerParams
from models.part.stairs.riser_params import RiserParams
from models.part.stairs.tread_params import TreadParams

from models.material.material import Material
from models.material.lumber import Lumber, lumber_2x12
from models.material.plywood import Plywood, plywood_3_8, plywood_5_8, plywood_1

from typing import Union as union

class StraightClosedRisersSawtoothStringerFlushStairsAssemblyParams(AssemblyParams):

    total_rise_height: float = Field(description="Total rise height")
    stairway_width: float = Field(description="Stairway width")
    number_of_steps_risers: int = Field(description="Number of steps risers")
    number_of_stringers: int = Field(default=2, description="Number of stringers")
    stringer_placement_from_top: float = Field(init=False, default=None, validate_default=False, description="Stringer placement from top")

    first_step_riser_height: float = Field( description="First step riser height")
    last_tread_depth: float = Field( description="Last tread depth")

    step_riser_height: float = Field( description="step riser height")
    tread_depth: float = Field(description="tread depth")

    tread_overhang_nosing_depth: float = Field(default=0.0, description="Tread overhang nosing depth")
    tread_overhang_side_depth: float = Field(default=0.0, description="Tread overhang side depth")


    first_riser_material : Plywood = Field(default=plywood_3_8, description="Material of the first riser, e.g., Plywood, etc.")
    riser_material : Plywood = Field(default=plywood_3_8, description="Material of the riser, e.g., Plywood, etc.")
    last_riser_material : Plywood = Field(default=plywood_5_8, description="Material of the last riser, e.g., Plywood, etc.")
    tread_material : Plywood = Field(default=plywood_1, description="Material of the tread, e.g., Plywood, etc.")
    last_tread_material : Plywood = Field(default=plywood_1, description="Material of the last tread, e.g., Plywood, etc.")
    stringer_material: Lumber = Field(default=lumber_2x12, description="Material of the stringer, e.g., Lumber, etc.")


    kicker_params: KickerParams = Field(init=False, default=None, validate_default=False, description="Parameters for the kicker")
    riser_params: RiserParams = Field(init=False, default=None, validate_default=False, description="Parameters for the risers")
    tread_params: TreadParams = Field(init=False, default=None, validate_default=False, description="Parameters for the treads")
    first_riser_params: RiserParams = Field(init=False, default=None, validate_default=False, description="Parameters for the first riser")
    last_tread_params: TreadParams = Field(init=False, default=None, validate_default=False, description="Parameters for the last tread")
   
    sawtooth_stringer_params: SawtoothStringerParams = Field(init=False, default=None, validate_default=False, description="Parameters for the sawtooth stringer")

    @model_validator(mode='after')
    def compute_params(self) -> 'StraightClosedRisersSawtoothStringerFlushStairsAssemblyParams':



        if self.kicker_params is None:
            self.kicker_params = KickerParams(
                job_name=self.job_name,
                part_name="kicker",
                kicker_height=0,
                kicker_depth=0,
                kicker_length=self.stairway_width
            )

        if self.riser_params is None:
            self.riser_params = RiserParams(
                job_name=self.job_name,
                part_name="riser",
                riser_height=self.step_riser_height,
                riser_length=self.stairway_width,
                material=self.riser_material
            )

        if self.tread_params is None:
            self.tread_params = TreadParams(
                job_name=self.job_name,
                part_name="tread",
                tread_depth=self.tread_depth,
                tread_length=self.stairway_width,
                material=self.tread_material
            )

        if self.first_riser_params is None:
            self.first_riser_params = RiserParams(
                job_name=self.job_name,
                part_name="first_riser",
                riser_height=self.first_step_riser_height,
                riser_length=self.stairway_width,
                material=self.first_riser_material
            )

        if self.last_tread_params is None:
            self.last_tread_params = TreadParams(
                job_name=self.job_name,
                part_name="last_tread",
                tread_depth=self.last_tread_depth,
                tread_length=self.stairway_width,
                material=self.last_tread_material
            )



        if self.sawtooth_stringer_params is None:
            self.sawtooth_stringer_params = SawtoothStringerParams(
                job_name=self.job_name,
                part_name="sawtooth_stringer",

                first_step_rise_height=self.first_riser_params.riser_height,
                last_step_run_depth=self.last_tread_params.tread_depth - self.tread_overhang_nosing_depth-self.riser_params.riser_thickness,

                step_rise_height=self.riser_params.riser_height,
                step_run_depth=self.tread_params.tread_depth - self.tread_overhang_nosing_depth ,


                number_of_stringer_run=self.number_of_steps_risers,

                kicker_height=self.kicker_params.kicker_height,
                kicker_depth=self.kicker_params.kicker_depth,

                material=self.stringer_material

            )



        self.stringer_placement_from_top =self.total_rise_height - self.sawtooth_stringer_params.stringer_total_rise
          

        # if abs(self.sawtooth_stringer_params.stringer_total_rise - (self.total_rise_height - self.last_tread_params.tread_thickness)) > 0.1:

        #         print( f"stringer_total_rise {self.sawtooth_stringer_params.stringer_total_rise} != {self.total_rise_height - self.last_tread_params.tread_thickness}")
        #         raise ValueError(
        #             f"sawtooth_stringer_params.stringer_total_rise must be within 0.1 of total_rise_height - last_tread_params.tread_thickness "
        #             f"{self.sawtooth_stringer_params.stringer_total_rise} != {self.total_rise_height - self.last_tread_params.tread_thickness}"
        #         )

        return self

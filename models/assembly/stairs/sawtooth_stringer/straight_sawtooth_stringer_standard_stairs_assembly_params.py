

from pydantic import BaseModel, Field, model_validator

from models.assembly.assembly_params import AssemblyParams

from models.part.stairs.kicker_params import KickerParams
from models.part.stairs.sawtooth_stringer_params import SawtoothStringerParams
from models.part.stairs.riser_params import RiserParams
from models.part.stairs.tread_params import TreadParams

from models.material.material import Material
from models.material.lumber import Lumber, lumber_2x12, lsl_2x12
from models.material.plywood import Plywood, plywood_3_8, plywood_5_8, plywood_1

from typing import Union as union

class StraightSawtoothStringerStandardStairsAssemblyParams(AssemblyParams):


    total_assembly_rise_height: float = Field(init=False, default=None, validate_default=False, description="Total rise height")
    total_assembly_run_depth: float = Field(init=False, default=None, validate_default=False, description="Total run depth")

    stairway_width: float = Field(description="Stairway width")
    number_of_steps: int = Field(description="Number of steps")


    typical_tread_depth: float = Field(description="Tread depth")
    tread_overhang_nosing_depth: float = Field(default=0.0, description="Tread overhang nosing depth")
    tread_overhang_side_depth: float = Field(default=0.0, description="Tread overhang side depth")
    typical_tread_material : Plywood = Field(default=plywood_1, description="Material of the tread, e.g., Plywood, etc.")
    typical_tread_params: TreadParams = Field(init=False, default=None, validate_default=False, description="Parameters for the treads")

    last_tread_depth: float = Field( description="Last tread depth")
    last_tread_material : Plywood = Field(default=plywood_1, description="Material of the last tread, e.g., Plywood, etc.")
    last_tread_params: TreadParams = Field(init=False, default=None, validate_default=False, description="Parameters for the last tread")
    


    open_riser: bool = Field(default=False, description="Open Riser")
    typical_riser_height: float = Field( description="Riser height")
    typical_riser_material : Plywood = Field(default=plywood_3_8, description="Material of the riser, e.g., Plywood, etc.")  
    typical_riser_params: RiserParams = Field(init=False, default=None, validate_default=False, description="Parameters for the risers")

    first_riser_height: float = Field( description="First riser height")
    first_riser_material : Plywood = Field(default=plywood_3_8, description="Material of the first riser, e.g., Plywood, etc.")
    first_riser_params: RiserParams = Field(init=False, default=None, validate_default=False, description="Parameters for the first riser")  

    last_riser_hanger_height: float = Field( description="Last riser hanger height")
    last_riser_hanger_material : Plywood = Field(default=plywood_5_8, description="Material of the last riser hanger, e.g., Plywood, etc.")
    last_riser_hanger_params: RiserParams = Field(init=False, default=None, validate_default=False, description="Parameters for the last riser hanger")


    kicker_params: KickerParams = Field(init=False, default=None, validate_default=False, description="Parameters for the kicker")


    number_of_stringers: int = Field(default=2, description="Number of stringers")
    stringer_placement_from_top: float = Field(init=False, default=None, validate_default=False, description="Stringer placement from top")
    stringer_material: Lumber = Field(default=lsl_2x12, description="Material of the stringer, e.g., Lumber, etc.")  
    sawtooth_stringer_params: SawtoothStringerParams = Field(init=False, default=None, validate_default=False, description="Parameters for the sawtooth stringer")




    @model_validator(mode='after')
    def compute(self) -> 'StraightSawtoothStringerStandardStairsAssemblyParams':


        self.kicker_params = KickerParams(
            job_name=self.job_name,
            part_name="kicker",
            kicker_height=0,
            kicker_depth=0,
            kicker_length=self.stairway_width
        )


        self.typical_riser_params = RiserParams(
            job_name=self.job_name,
            part_name="riser",
            riser_height=self.typical_riser_height,
            riser_length=self.stairway_width,
            riser_material=self.typical_riser_material
        )


        self.typical_tread_params = TreadParams(
            job_name=self.job_name,
            part_name="tread",
            tread_depth=self.typical_tread_depth,
            tread_length=self.stairway_width,
            tread_material=self.typical_tread_material
        )

        self.first_riser_params = RiserParams(
            job_name=self.job_name,
            part_name="first_riser",
            riser_height=self.first_riser_height,
            riser_length=self.stairway_width,
            riser_material=self.first_riser_material
        )


        self.last_tread_params = TreadParams(
            job_name=self.job_name,
            part_name="last_tread",
            tread_depth=self.last_tread_depth,
            tread_length=self.stairway_width,
            tread_material=self.last_tread_material
        )


        self.last_riser_hanger_params = RiserParams(
            job_name=self.job_name,
            part_name="last_riser_hanger",
            riser_height=self.last_riser_hanger_height,
            riser_length=self.stairway_width,
            riser_material=self.last_riser_hanger_material
        )




        if not self.open_riser:
            # closed Riser Stringer

            self.sawtooth_stringer_params = SawtoothStringerParams(
                job_name=self.job_name,
                part_name="sawtooth_stringer",

                first_stringer_rise_height=self.first_riser_params.riser_height,
                last_stringer_run_depth=self.last_tread_params.tread_depth - self.tread_overhang_nosing_depth - self.typical_riser_params.riser_thickness, 

                typical_stringer_rise_height=self.typical_riser_params.riser_height,
                typical_stringer_run_depth=self.typical_tread_params.tread_depth - self.tread_overhang_nosing_depth,


                number_of_stringer_rise=self.number_of_steps - 1,

                stringer_kicker_height=self.kicker_params.kicker_height,
                stringer_kicker_depth=self.kicker_params.kicker_depth,

                stringer_material=self.stringer_material

            )


        else:
            # open Riser Stringer

            self.sawtooth_stringer_params = SawtoothStringerParams(
                job_name=self.job_name,
                part_name="sawtooth_stringer",

                first_stringer_rise_height=self.first_riser_params.riser_height,
                last_stringer_run_depth=self.last_tread_params.tread_depth - self.tread_overhang_nosing_depth, 

                typical_stringer_rise_height=self.typical_riser_params.riser_height,
                typical_stringer_run_depth=self.typical_tread_params.tread_depth - self.tread_overhang_nosing_depth,


                number_of_stringer_rise=self.number_of_steps - 1,

                stringer_kicker_height=self.kicker_params.kicker_height,
                stringer_kicker_depth=self.kicker_params.kicker_depth,

                stringer_material=self.stringer_material

            )




        if not self.open_riser:
            # closed Riser
            self.total_assembly_run_depth = self.first_riser_params.riser_thickness + self.sawtooth_stringer_params.total_stringer_run_depth + self.last_riser_hanger_params.riser_thickness
        else:
            # open Riser
            self.total_assembly_run_depth = self.sawtooth_stringer_params.total_stringer_run_depth + self.last_riser_hanger_params.riser_thickness

        self.total_assembly_rise_height = self.first_riser_params.riser_height + ((self.number_of_steps - 2) * self.typical_riser_params.riser_height) + self.typical_riser_params.riser_height + self.typical_tread_params.tread_thickness

        self.stringer_placement_from_top = self.total_assembly_rise_height - self.sawtooth_stringer_params.total_stringer_rise_height

        return self



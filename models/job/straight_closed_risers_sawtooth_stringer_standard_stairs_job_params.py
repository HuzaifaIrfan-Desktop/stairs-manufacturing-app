
from pydantic import BaseModel, Field, model_validator

from models.job.job_params import JobInputParams

from models.assembly.stairs.sawtooth_stringer.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params import StraightClosedRisersSawtoothStringerStandardStairsAssemblyParams


class StraightClosedRisersSawtoothStringerStandardStairsJobInputParams(JobInputParams):
    job_name: str = "Default Standard Stairs Job"

    total_rise_height: float = Field(default=122.0, description="Total rise height")
    stairway_width: float = Field(default=36.75, description="Stairway width")
    number_of_steps_risers: int = Field(default=16, description="Number of steps risers")
    number_of_stringers: int = Field(default=2, description="Number of stringers")
   
    top_floor_thickness: float = Field(default=1.0,description="Top floor thickness")

    first_step_riser_height: float = Field(default=6.63, description="First step riser height")
    last_step_riser_height: float = Field(default=7.63, description="Last step riser height")
    last_tread_depth: float = Field(default=11.5, description="Last tread depth")

    step_riser_height: float = Field(default=7.63, description="step riser height")
    tread_depth: float = Field(default=11.5,description="tread depth")

    tread_overhang_nosing_depth: float = Field(default=0.0, description="Tread overhang nosing depth")
    tread_overhang_side_depth: float = Field(default=0.0, description="Tread overhang side depth")



class StraightClosedRisersSawtoothStringerStandardStairsJobOutputParams(StraightClosedRisersSawtoothStringerStandardStairsJobInputParams):
    standard_stairs_assembly_params:StraightClosedRisersSawtoothStringerStandardStairsAssemblyParams = Field(init=False, default=None, validate_default=False, description="Standard stairs assembly parameters")

    @model_validator(mode='after')
    def compute_params(self) -> 'StraightClosedRisersSawtoothStringerStandardStairsJobOutputParams':

        self.standard_stairs_assembly_params = StraightClosedRisersSawtoothStringerStandardStairsAssemblyParams(
            **self.model_dump(),
            assembly_name="StandardStairsAssembly",
        )

        return self

from pydantic import BaseModel, Field, model_validator

from models.assembly.assembly_params import AssemblyParams

from models.part.stairs.kicker_params import KickerParams
from models.part.stairs.sawtooth_stringer_params import SawtoothStringerParams
from models.part.stairs.riser_params import RiserParams
from models.part.stairs.tread_params import TreadParams

class StraightClosedRisersSawtoothStringerStandardStairsAssemblyParams(AssemblyParams):

    total_riser_height: float = Field(description="Total riser height")
    stairway_width: float = Field(description="Stairway width")
    number_of_steps_risers: int = Field(description="Number of steps risers")

    first_riser_material: str = Field(default="wood", description="Material for the first riser")

    first_step_riser_height: float = Field(default=0.0, description="First step riser height")
    last_step_riser_height: float = Field(default=0.0, description="Last step riser height")
    last_tread_depth: float = Field(default=0.0, description="Last tread depth")

    step_riser_height: float = Field(default=0.0, description="step riser height")
    tread_depth: float = Field(default=0.0, description="tread depth")

    tread_overhang_nosing_depth: float = Field(default=0.0, description="Tread overhang nosing depth")


    kicker_params: KickerParams = Field(init=False, default=None, validate_default=False, description="Parameters for the kicker")
    
    riser_params: RiserParams = Field(init=False, default=None, validate_default=False, description="Parameters for the risers")
    tread_params: TreadParams = Field(init=False, default=None, validate_default=False, description="Parameters for the treads")

    first_riser_params: RiserParams = Field(init=False, default=None, validate_default=False, description="Parameters for the first riser")
    last_tread_params: TreadParams = Field(init=False, default=None, validate_default=False, description="Parameters for the last tread")
    last_riser_params: RiserParams = Field(init=False, default=None, validate_default=False, description="Parameters for the last riser")

    sawtooth_stringer_params: SawtoothStringerParams = Field(init=False, default=None, validate_default=False, description="Parameters for the sawtooth stringer")

    @model_validator(mode='after')
    def compute_params(self) -> 'StraightClosedRisersSawtoothStringerStandardStairsAssemblyParams':



        if self.kicker_params is None:
            self.kicker_params = KickerParams(
                job_name=self.job_name,
                part_name="kicker",
                kicker_height=1,
                kicker_depth=1,
                kicker_length=self.stairway_width
            )

        if self.riser_params is None:
            self.riser_params = RiserParams(
                job_name=self.job_name,
                part_name="riser",
                riser_height=self.step_riser_height,
                riser_length=self.stairway_width
            )

        if self.tread_params is None:
            self.tread_params = TreadParams(
                job_name=self.job_name,
                part_name="tread",
                tread_depth=self.tread_depth,
                tread_length=self.stairway_width
            )

        if self.first_riser_params is None:
            self.first_riser_params = RiserParams(
                job_name=self.job_name,
                part_name="first_riser",
                riser_height=self.first_step_riser_height,
                riser_length=self.stairway_width
            )

        if self.last_tread_params is None:
            self.last_tread_params = TreadParams(
                job_name=self.job_name,
                part_name="last_tread",
                tread_depth=self.last_tread_depth,
                tread_length=self.stairway_width
            )

        if self.last_riser_params is None:
            self.last_riser_params = RiserParams(
                job_name=self.job_name,
                part_name="last_riser",
                riser_height=self.last_step_riser_height,
                riser_length=self.stairway_width
            )


        if self.sawtooth_stringer_params is None:
            self.sawtooth_stringer_params = SawtoothStringerParams(
                job_name=self.job_name,
                part_name="sawtooth_stringer",

                first_step_rise_height=self.first_riser_params.riser_height,
                last_step_run_depth=self.last_tread_params.tread_depth - self.tread_overhang_nosing_depth,

                step_rise_height=self.riser_params.riser_height,
                step_run_depth=self.tread_params.tread_depth - self.tread_overhang_nosing_depth,


                number_of_stringer_run=self.number_of_steps_risers - 1,

                stringer_placement_from_top=0.0,

                kicker_height=self.kicker_params.kicker_height,
                kicker_depth=self.kicker_params.kicker_depth,

            )


        return self



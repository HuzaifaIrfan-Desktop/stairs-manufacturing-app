
from pydantic import BaseModel, Field, model_validator

from models.assembly.assembly_params import AssemblyParams

from models.part.stairs.kicker_params import KickerParams
from models.part.stairs.sawtooth_stringer_params import SawtoothStringerParams
from models.part.stairs.riser_params import RiserParams
from models.part.stairs.tread_params import TreadParams

class StraightClosedRisersSawtoothStringerStandardStairsAssemblyParams(AssemblyParams):
    
    kicker_params: KickerParams = Field(init=False, default=None, validate_default=False, description="Parameters for the kicker")
    sawtooth_stringer_params: SawtoothStringerParams = Field(init=False, default=None, validate_default=False, description="Parameters for the sawtooth stringer")
    riser_params: RiserParams = Field(init=False, default=None, validate_default=False, description="Parameters for the risers")
    tread_params: TreadParams = Field(init=False, default=None, validate_default=False, description="Parameters for the treads")

    first_riser_params: RiserParams = Field(init=False, default=None, validate_default=False, description="Parameters for the first riser")
    last_tread_params: TreadParams = Field(init=False, default=None, validate_default=False, description="Parameters for the last tread")
    last_riser_params: RiserParams = Field(init=False, default=None, validate_default=False, description="Parameters for the last riser")


    @model_validator(mode='after')
    def compute_params(self) -> 'StraightClosedRisersSawtoothStringerStandardStairsAssemblyParams':

        if self.kicker_params is None:
            self.kicker_params = KickerParams(
                job_name=self.job_name,
                part_name="kicker",
                kicker_height=1,
                kicker_depth=1,
                kicker_length=36
            )

        if self.sawtooth_stringer_params is None:
            self.sawtooth_stringer_params = SawtoothStringerParams(
                job_name=self.job_name,
                part_name="sawtooth_stringer",

                first_step_rise_height=7,
                last_step_run_depth=10,

                step_rise_height=7,
                step_run_depth=10,

                number_of_stringer_run=12,

                stringer_placement_from_top=5,

                kicker_height=1,
                kicker_depth=1,
                

            )

        if self.riser_params is None:
            self.riser_params = RiserParams(
                job_name=self.job_name,
                part_name="riser",
                riser_height=7,
                riser_length=36
            )

        if self.tread_params is None:
            self.tread_params = TreadParams(
                job_name=self.job_name,
                part_name="tread",
                tread_depth=10,
                tread_length=36
            )

        if self.first_riser_params is None:
            self.first_riser_params = RiserParams(
                job_name=self.job_name,
                part_name="first_riser",
                riser_height=7,
                riser_length=36
            )

        if self.last_tread_params is None:
            self.last_tread_params = TreadParams(
                job_name=self.job_name,
                part_name="last_tread",
                tread_depth=10,
                tread_length=36
            )

        if self.last_riser_params is None:
            self.last_riser_params = RiserParams(
                job_name=self.job_name,
                part_name="last_riser",
                riser_height=7,
                riser_length=36
            )



        return self



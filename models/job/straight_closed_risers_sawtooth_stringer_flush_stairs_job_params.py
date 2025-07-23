

from pydantic import BaseModel, Field, model_validator

from models.job.job_params import JobInputParams

from models.assembly.stairs.sawtooth_stringer.straight_closed_risers_sawtooth_stringer_flush_stairs_assembly_params import StraightClosedRisersSawtoothStringerFlushStairsAssemblyParams


from models.material.lumber import available_lumbers
from models.material.plywood import available_plywoods
from models.material import available_materials

class StraightClosedRisersSawtoothStringerFlushStairsJobInputParams(JobInputParams):
    job_name: str = "Default Flush Stairs Job"

    total_rise_height: float = Field(default=122.0,description="Total rise height")
    stairway_width: float = Field(default=36.75,description="Stairway width")
    number_of_steps_risers: int = Field(default=16,description="Number of steps risers")
    number_of_stringers: int = Field(default=2, description="Number of stringers")

    flush_stairs_assembly_params:StraightClosedRisersSawtoothStringerFlushStairsAssemblyParams = Field(init=False, default=None, validate_default=False, description="Flush stairs assembly parameters")


    first_step_riser_height: float = Field(default=6.63, description="First step riser height")
    last_tread_depth: float = Field(default=10.78, description="Last tread depth")

    step_riser_height: float = Field(default=7.63, description="step riser height")

    tread_depth: float = Field(default=10.78,description="tread depth")

    tread_overhang_nosing_depth: float = Field(default=0.0, description="Tread overhang nosing depth")
    tread_overhang_side_depth: float = Field(default=0.0, description="Tread overhang side depth")


    stringer_material_name: str = Field(
        default='2x12 Lumber',
        description="Stringer material",
        json_schema_extra={"enum": list(available_lumbers.keys())}
    )

    riser_material_name: str = Field(
        default='3/8" Plywood',
        description="Riser material",
        json_schema_extra={"enum": list(available_plywoods.keys())}
    )

    tread_material_name: str = Field(
        default='1" Plywood',
        description="Tread material",
        json_schema_extra={"enum": list(available_materials.keys())}
    )

class StraightClosedRisersSawtoothStringerFlushStairsJobOutputParams(StraightClosedRisersSawtoothStringerFlushStairsJobInputParams):


    @model_validator(mode='after')
    def compute_params(self) -> 'StraightClosedRisersSawtoothStringerFlushStairsJobOutputParams':



        self.flush_stairs_assembly_params = StraightClosedRisersSawtoothStringerFlushStairsAssemblyParams(
            **self.model_dump(),
            assembly_name="FlushStairsAssembly",

            tread_material= available_materials[self.tread_material_name].model_dump(),
            last_tread_material= available_materials[self.tread_material_name].model_dump(),
            first_riser_material= available_materials[self.riser_material_name].model_dump(),
            riser_material = available_materials[self.riser_material_name].model_dump(),
            stringer_material = available_materials[self.stringer_material_name].model_dump(),
        )

        return self
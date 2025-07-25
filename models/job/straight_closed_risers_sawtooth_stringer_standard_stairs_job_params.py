
from pydantic import BaseModel, Field, model_validator

from models.job.job_params import JobInputParams

from models.assembly.stairs.sawtooth_stringer.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params import StraightClosedRisersSawtoothStringerStandardStairsAssemblyParams

from models.material.lumber import available_lumbers
from models.material.plywood import available_plywoods
from models.material import available_materials

class StraightClosedRisersSawtoothStringerStandardStairsJobInputParams(JobInputParams):
    job_name: str = "Default Standard Stairs Job"

    stairway_width: float = Field(default=36.75, description="Stairway width")
    number_of_stringers: int = Field(default=2, description="Number of stringers")

    tread_overhang_nosing_depth: float = Field(default=0.0, description="Tread overhang nosing depth")
    tread_overhang_side_depth: float = Field(default=0.0, description="Tread overhang side depth")



    number_of_steps: int = Field(default=16, description="Number of steps")
    first_riser_height: float = Field(default=6.63, description="First riser height")
    last_riser_hanger_height: float = Field(default=13.25, description="Last riser hanger height")
    last_tread_depth: float = Field(default=11.5, description="Last tread depth")

    typical_riser_height: float = Field(default=7.63, description="Riser height")
    typical_tread_depth: float = Field(default=11.5,description="Tread depth")



    stringer_material_name: str = Field(
        default='2x12 LSL',
        description="Stringer material",
        json_schema_extra={"enum": list(available_lumbers.keys())}
    )

    riser_material_name: str = Field(
        default='3/8" Plywood',
        description="Riser material",
        json_schema_extra={"enum": list(available_plywoods.keys())}
    )


    last_riser_hanger_material_name: str = Field(
        default='5/8" Plywood',
        description="Riser material",
        json_schema_extra={"enum": list(available_plywoods.keys())}
    )

    tread_material_name: str = Field(
        default='1" Plywood',
        description="Tread material",
        json_schema_extra={"enum": list(available_materials.keys())}
    )

class StraightClosedRisersSawtoothStringerStandardStairsJobOutputParams(StraightClosedRisersSawtoothStringerStandardStairsJobInputParams):
    standard_stairs_assembly_params:StraightClosedRisersSawtoothStringerStandardStairsAssemblyParams = Field(init=False, default=None, validate_default=False, description="Standard stairs assembly parameters")

    @model_validator(mode='after')
    def compute_params(self) -> 'StraightClosedRisersSawtoothStringerStandardStairsJobOutputParams':


        typical_tread_material= available_materials[self.tread_material_name].model_dump()
        last_tread_material= available_materials[self.tread_material_name].model_dump()
        first_riser_material= available_materials[self.riser_material_name].model_dump()
        typical_riser_material = available_materials[self.riser_material_name].model_dump()
        last_riser_hanger_material = available_materials[self.last_riser_hanger_material_name].model_dump()
        stringer_material = available_materials[self.stringer_material_name].model_dump()


        self.standard_stairs_assembly_params = StraightClosedRisersSawtoothStringerStandardStairsAssemblyParams(
            **self.model_dump(),
            assembly_name="StandardStairsAssembly",

            typical_tread_material=typical_tread_material,
            last_tread_material=last_tread_material,
            first_riser_material=first_riser_material,
            typical_riser_material=typical_riser_material,
            last_riser_hanger_material=last_riser_hanger_material,
            stringer_material=stringer_material

        )

        return self
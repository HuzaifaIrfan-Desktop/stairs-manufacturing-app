
from pydantic import BaseModel, Field, model_validator

from models.job.job_params import JobInputParams

from models.assembly.stairs.sawtooth_stringer.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params import StraightClosedRisersSawtoothStringerStandardStairsAssemblyParams

from models.material.lumber import available_lumbers
from models.material.plywood import available_plywoods
from models.material import available_materials

class StraightClosedRisersSawtoothStringerStandardStairsJobInputParams(JobInputParams):
    job_name: str  = Field(default="Default Standard Stairs Job", description="Job Name")

    stairway_width: float = Field(default=36.75, description="Stairway Width (in)")
    number_of_stringers: int = Field(default=2, description="Number of Stringers")

    tread_overhang_nosing_depth: float = Field(default=0.0, description="Tread Overhang Nosing Depth (in)")
    tread_overhang_side_depth: float = Field(default=0.0, description="Tread Overhang Side Depth (in)")



    number_of_steps: int = Field(default=16, description="Number of Steps")
    first_riser_height: float = Field(default=6.63, description="First Riser Height (in)")
    last_riser_hanger_height: float = Field(default=13.25, description="Last Riser Hanger Height (in)")
    last_tread_depth: float = Field(default=11.5, description="Last Tread Depth (in)")

    typical_riser_height: float = Field(default=7.63, description="Riser Height (in)")
    typical_tread_depth: float = Field(default=11.5,description="Tread Depth (in)")



    stringer_material_name: str = Field(
        default='2x12 LSL',
        description="Stringer Material",
        json_schema_extra={"enum": list(available_lumbers.keys())}
    )

    riser_material_name: str = Field(
        default='3/8" Plywood',
        description="Riser Material",
        json_schema_extra={"enum": list(available_plywoods.keys())}
    )


    last_riser_hanger_material_name: str = Field(
        default='5/8" Plywood',
        description="Riser Hanger Material",
        json_schema_extra={"enum": list(available_plywoods.keys())}
    )

    tread_material_name: str = Field(
        default='1" Plywood',
        description="Tread Material",
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
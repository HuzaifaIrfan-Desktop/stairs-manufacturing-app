
from pydantic import BaseModel, Field, model_validator

from models.job.job_params import JobInputParams

from models.assembly.stairs.sawtooth_stringer.straight_sawtooth_stringer_standard_stairs_assembly_params import StraightSawtoothStringerStandardStairsAssemblyParams

from models.material.lumber import available_lumbers
from models.material.plywood import available_plywoods
from models.material import available_materials

class StraightSawtoothStringerStandardStairsJobInputParams(JobInputParams):
    job_name: str  = Field(default="Default Standard Stairs Job", description="Job Name")

    assembly_form_spacer: str = Field(default="Assembly Form Spacer", description="Assembly Inputs", exclude=True)
    total_rise_height: float = Field(default=122.0, description="Total Rise Height (in)")
    number_of_steps: int = Field(default=16,description="Number of Steps")
    stairway_width: float = Field(default=36.75, description="Stairway Width (in)")



    tread_form_spacer: str = Field(default="Tread Form Spacer", description="Tread Inputs", exclude=True)
    tread_depth: float = Field(default=10.78, description="Tread Depth (in)")
    tread_overhang_nosing_depth: float = Field(default=0.0, description="Tread Overhang Nosing Depth (in)")
    tread_overhang_side_depth: float = Field(default=0.0, description="Tread Overhang Side Depth (in)")
    tread_material_name: str = Field(
        default='1" Plywood',
        description="Tread Material",
        json_schema_extra={"enum": list(available_materials.keys())}
    )

    riser_form_spacer: str = Field(default="Riser Form Spacer", description="Riser Inputs", exclude=True)
    open_riser: bool = Field(default=False, description="Open Riser")
    riser_material_name: str = Field(
        default='3/8" Plywood',
        description="Riser Material",
        json_schema_extra={"enum": list(available_plywoods.keys())}
    )

    hanger_form_spacer: str = Field(default="Hanger Form Spacer", description="Hanger Inputs", exclude=True)
    last_riser_hanger_height: float = Field(default=13.25, description="Last Riser Hanger Height (in)")
    last_riser_hanger_material_name: str = Field(
        default='5/8" Plywood',
        description="Riser Hanger Material",
        json_schema_extra={"enum": list(available_plywoods.keys())}
    )

    stringer_form_spacer: str = Field(default="Stringer Form Spacer", description="Stringer Inputs", exclude=True)
    number_of_stringers: int = Field(default=2, description="Number of Stringers")
    stringer_material_name: str = Field(
        default='2x12 LSL',
        description="Stringer Material",
        json_schema_extra={"enum": list(available_lumbers.keys())}
    )



class StraightSawtoothStringerStandardStairsJobOutputParams(StraightSawtoothStringerStandardStairsJobInputParams):
    standard_stairs_assembly_params:StraightSawtoothStringerStandardStairsAssemblyParams = Field(init=False, default=None, validate_default=False, description="Standard stairs assembly parameters")

    @model_validator(mode='after')
    def compute(self) -> 'StraightSawtoothStringerStandardStairsJobOutputParams':


        tread_material= available_materials[self.tread_material_name].model_dump()
        riser_material = available_materials[self.riser_material_name].model_dump()
        last_riser_hanger_material = available_materials[self.last_riser_hanger_material_name].model_dump()
        stringer_material = available_materials[self.stringer_material_name].model_dump()




        self.standard_stairs_assembly_params = StraightSawtoothStringerStandardStairsAssemblyParams(
            job_name=self.job_name,
            builder_name=self.builder_name,
            assembly_name="StandardStairsAssembly",
            
            stairway_width=self.stairway_width,
            number_of_steps=self.number_of_steps,

            total_opening_rise_height= self.total_rise_height,


            tread_depth=self.tread_depth,
            tread_overhang_nosing_depth=self.tread_overhang_nosing_depth,
            tread_overhang_side_depth=self.tread_overhang_side_depth,
            tread_material=tread_material,
     
            open_riser=self.open_riser,
            riser_material=riser_material,

       
            last_riser_hanger_height=self.last_riser_hanger_height,
            last_riser_hanger_material=last_riser_hanger_material,


            number_of_stringers=self.number_of_stringers,
            stringer_material=stringer_material

        )

        return self
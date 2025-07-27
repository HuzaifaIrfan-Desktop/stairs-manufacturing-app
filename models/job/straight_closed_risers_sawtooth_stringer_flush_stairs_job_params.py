

from pydantic import BaseModel, Field, model_validator

from models.job.job_params import JobInputParams

from models.assembly.stairs.sawtooth_stringer.straight_closed_risers_sawtooth_stringer_flush_stairs_assembly_params import StraightClosedRisersSawtoothStringerFlushStairsAssemblyParams


from models.material.lumber import available_lumbers
from models.material.plywood import available_plywoods
from models.material import available_materials

class StraightClosedRisersSawtoothStringerFlushStairsJobInputParams(JobInputParams):
    job_name: str = Field(default="Default Flush Stairs Job", description="Job Name")

    total_rise_height: float = Field(default=122.0, description="Total Rise Height (in)")
    number_of_steps: int = Field(default=16,description="Number of Steps")
    stairway_width: float = Field(default=36.75,description="Stairway Width (in)")

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

    stringer_form_spacer: str = Field(default="Stringer Form Spacer", description="Stringer Inputs", exclude=True)
    number_of_stringers: int = Field(default=2, description="Number of Stringers")
    stringer_material_name: str = Field(
        default='2x12 LSL',
        description="Stringer Material",
        json_schema_extra={"enum": list(available_lumbers.keys())}
    )


class StraightClosedRisersSawtoothStringerFlushStairsJobOutputParams(StraightClosedRisersSawtoothStringerFlushStairsJobInputParams):


    flush_stairs_assembly_params:StraightClosedRisersSawtoothStringerFlushStairsAssemblyParams = Field(init=False, default=None, validate_default=False, description="Flush stairs assembly parameters")


    @model_validator(mode='after')
    def compute(self) -> 'StraightClosedRisersSawtoothStringerFlushStairsJobOutputParams':

        typical_tread_material= available_materials[self.tread_material_name].model_dump()
        last_tread_material= available_materials[self.tread_material_name].model_dump()
        first_riser_material= available_materials[self.riser_material_name].model_dump()
        typical_riser_material = available_materials[self.riser_material_name].model_dump()
        stringer_material = available_materials[self.stringer_material_name].model_dump()

        last_tread_depth: float = self.tread_depth
        typical_tread_depth: float = self.tread_depth

        # Calculate riser heights from total rise and number of steps
        def calculate_flush_stair_riser_heights(
            total_rise: float,
            num_steps: int,
            tread_thickness: float
        ) -> dict:
            """
            Calculate first and typical riser heights for flush-mounted stairs.

            Args:
                total_rise: Total vertical height between floors (inches)
                num_steps: Total number of risers/steps
                tread_thickness: Thickness of each tread (inches)

            Returns:
                Dictionary with first_riser_height and typical_riser_height
            """

            typical_riser_height = total_rise / num_steps
            first_riser_height = typical_riser_height - tread_thickness

            return {
                "typical_riser_height": round(typical_riser_height, 2),
                "first_riser_height": round(first_riser_height, 2)
            }
        
        risers_heights_calculations = calculate_flush_stair_riser_heights(
            total_rise=self.total_rise_height,
            num_steps=self.number_of_steps,
            tread_thickness= available_materials[self.tread_material_name].thickness
        )

        typical_riser_height: float = risers_heights_calculations["typical_riser_height"]
        first_riser_height: float = risers_heights_calculations["first_riser_height"]


        if typical_riser_height >= 7.875:
            raise ValueError("Maximum allowed riser height is 7.875 inches. Please adjust the number of steps.")

        

        self.flush_stairs_assembly_params = StraightClosedRisersSawtoothStringerFlushStairsAssemblyParams(
            **self.model_dump(),
            assembly_name="FlushStairsAssembly",

            last_tread_depth=last_tread_depth,
            typical_tread_depth=typical_tread_depth,
            first_riser_height=first_riser_height,
            typical_riser_height=typical_riser_height,

            typical_tread_material=typical_tread_material,
            last_tread_material=last_tread_material,
            first_riser_material=first_riser_material,
            typical_riser_material=typical_riser_material,
            stringer_material=stringer_material

        )

        return self
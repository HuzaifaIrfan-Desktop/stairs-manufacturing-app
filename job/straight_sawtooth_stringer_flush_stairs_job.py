

from job.job import Job

from models.job.straight_sawtooth_stringer_flush_stairs_job_params import StraightSawtoothStringerFlushStairsJobInputParams, StraightSawtoothStringerFlushStairsJobOutputParams

from models.assembly.stairs.sawtooth_stringer.straight_sawtooth_stringer_flush_stairs_assembly_params import StraightSawtoothStringerFlushStairsAssemblyParams

from assembly.stairs.sawtooth_stringer.straight_sawtooth_stringer_flush_stairs_assembly import StraightSawtoothStringerFlushStairsAssembly


import cadquery as cq

from utils.math import inch_to_mm

from logger import job_logger

from part.top_floor_opening import TopFloorOpening
from models.part.top_floor_opening_params import TopFloorOpeningParams


class StraightSawtoothStringerFlushStairsJob(Job):
    def __init__(self, straight_sawtooth_stringer_flush_stairs_job_input_params:StraightSawtoothStringerFlushStairsJobInputParams):
        self.job_input_params = straight_sawtooth_stringer_flush_stairs_job_input_params


        self.job_output_params = StraightSawtoothStringerFlushStairsJobOutputParams(
            **self.job_input_params.model_dump()
        )

        self.flush_stairs_assembly_params = self.job_output_params.flush_stairs_assembly_params

        self.flush_stairs_assembly = StraightSawtoothStringerFlushStairsAssembly(self.flush_stairs_assembly_params)

        super().__init__(self.job_input_params)


    def _assemble(self):
        assembly_object = self.flush_stairs_assembly.get().val()

        # Add top floor opening if specified
        top_floor_opening_params = TopFloorOpeningParams(
            job_name=self.job_input_params.job_name, part_name="top_floor_opening",
            opening_length=self.flush_stairs_assembly_params.total_assembly_run_depth,
            opening_width=self.job_input_params.stairway_width,
            opening_top_position=self.job_input_params.total_rise_height
        )
        top_floor_opening = TopFloorOpening(top_floor_opening_params)
        top_floor_opening_object = top_floor_opening.get().val()

        compound = cq.Compound.makeCompound([assembly_object, top_floor_opening_object])
        self.cq_job_assembly = cq.Workplane(obj=compound)

    def export(self) -> str:
        # Export the job parameters to a file
        file_path = self.export_job_params()
        self.flush_stairs_assembly.export()

        return file_path
    
    def export_drawings(self) -> str:
        # Export the assembly to a file
        file_path = self.flush_stairs_assembly.export_drawings()
        return file_path
    
    def export_reports(self) -> str:
        # Export the assembly to a file
        file_path = self.flush_stairs_assembly.export_reports()
        return file_path
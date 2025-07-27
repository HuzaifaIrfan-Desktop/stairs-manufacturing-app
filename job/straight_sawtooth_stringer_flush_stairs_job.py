

from job.job import Job

from models.job.straight_sawtooth_stringer_flush_stairs_job_params import StraightSawtoothStringerFlushStairsJobInputParams, StraightSawtoothStringerFlushStairsJobOutputParams

from models.assembly.stairs.sawtooth_stringer.straight_sawtooth_stringer_flush_stairs_assembly_params import StraightSawtoothStringerFlushStairsAssemblyParams

from assembly.stairs.sawtooth_stringer.straight_sawtooth_stringer_flush_stairs_assembly import StraightSawtoothStringerFlushStairsAssembly


import cadquery as cq

from utils.math import inch_to_mm

from logger import job_logger

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
        assembly = self.flush_stairs_assembly.get().val()

        compound = cq.Compound.makeCompound([assembly])
        self.cq_job_assembly = cq.Workplane(obj=compound)

    def export(self) -> str:
        # Export the job parameters to a file
        file_path = self.export_job_params()
        self.flush_stairs_assembly.export()
        self.flush_stairs_assembly.export_cam()
        return file_path
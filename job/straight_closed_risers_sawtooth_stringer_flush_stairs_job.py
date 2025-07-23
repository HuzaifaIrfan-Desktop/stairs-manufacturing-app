

from job.job import Job

from models.job.straight_closed_risers_sawtooth_stringer_flush_stairs_job_params import StraightClosedRisersSawtoothStringerFlushStairsJobInputParams, StraightClosedRisersSawtoothStringerFlushStairsJobOutputParams

from models.assembly.stairs.sawtooth_stringer.straight_closed_risers_sawtooth_stringer_flush_stairs_assembly_params import StraightClosedRisersSawtoothStringerFlushStairsAssemblyParams

from assembly.stairs.sawtooth_stringer.straight_closed_risers_sawtooth_stringer_flush_stairs_assembly import StraightClosedRisersSawtoothStringerFlushStairsAssembly


import cadquery as cq

from utils.math import inch_to_mm

from logger import job_logger

class StraightClosedRisersSawtoothStringerFlushStairsJob(Job):
    def __init__(self, straight_closed_risers_sawtooth_stringer_flush_stairs_job_input_params:StraightClosedRisersSawtoothStringerFlushStairsJobInputParams):
        self.job_input_params = straight_closed_risers_sawtooth_stringer_flush_stairs_job_input_params


        self.job_output_params = StraightClosedRisersSawtoothStringerFlushStairsJobOutputParams(
            **self.job_input_params.model_dump()
        )

        self.flush_stairs_assembly_params = self.job_output_params.flush_stairs_assembly_params

        self.flush_stairs_assembly = StraightClosedRisersSawtoothStringerFlushStairsAssembly(self.flush_stairs_assembly_params)

        super().__init__(self.job_input_params)


    def _assemble(self):
        assembly = self.flush_stairs_assembly.get().val()

        compound = cq.Compound.makeCompound([assembly])
        self.cq_job_assembly = cq.Workplane(obj=compound)

    def export(self) -> str:
        # Export the job parameters to a file
        file_path = self.export_job_params()
        self.flush_stairs_assembly.export()
        return file_path
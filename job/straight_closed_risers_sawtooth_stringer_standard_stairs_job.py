

from job.job import Job

from models.job.straight_closed_risers_sawtooth_stringer_standard_stairs_job_params import StraightClosedRisersSawtoothStringerStandardStairsJobInputParams ,StraightClosedRisersSawtoothStringerStandardStairsJobOutputParams

from models.assembly.stairs.sawtooth_stringer.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params import StraightClosedRisersSawtoothStringerStandardStairsAssemblyParams

from assembly.stairs.sawtooth_stringer.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly import StraightClosedRisersSawtoothStringerStandardStairsAssembly

import cadquery as cq
from utils.math import inch_to_mm

from logger import job_logger

class StraightClosedRisersSawtoothStringerStandardStairsJob(Job):
    def __init__(self, straight_closed_risers_sawtooth_stringer_standard_stairs_job_input_params:StraightClosedRisersSawtoothStringerStandardStairsJobInputParams):
        self.job_input_params = straight_closed_risers_sawtooth_stringer_standard_stairs_job_input_params
        job_logger.info(f"Initializing StraightClosedRisersSawtoothStringerStandardStairsJob with params: {self.job_input_params}")

        self.job_output_params = StraightClosedRisersSawtoothStringerStandardStairsJobOutputParams(
            **self.job_input_params.model_dump()
        )

        self.standard_stairs_assembly_params = self.job_output_params.standard_stairs_assembly_params

        self.standard_stairs_assembly = StraightClosedRisersSawtoothStringerStandardStairsAssembly(self.standard_stairs_assembly_params)

        super().__init__(self.job_input_params)


    def _assemble(self):
        assembly = self.standard_stairs_assembly.get().val()

        compound = cq.Compound.makeCompound([assembly])
        self.cq_job_assembly = cq.Workplane(obj=compound)

    def export(self) -> str:
        # Export the job parameters to a file
        file_path = self.export_job_params()
        self.standard_stairs_assembly.export()
        return file_path
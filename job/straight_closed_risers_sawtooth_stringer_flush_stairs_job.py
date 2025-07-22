

from job.job import Job

from models.job.straight_closed_risers_sawtooth_stringer_flush_stairs_job_params import StraightClosedRisersSawtoothStringerFlushStairsJobInputParams

class StraightClosedRisersSawtoothStringerFlushStairsJob(Job):
    def __init__(self, straight_closed_risers_sawtooth_stringer_flush_stairs_job_input_params:StraightClosedRisersSawtoothStringerFlushStairsJobInputParams):
        self.straight_closed_risers_sawtooth_stringer_flush_stairs_job_input_params = straight_closed_risers_sawtooth_stringer_flush_stairs_job_input_params

        super().__init__(straight_closed_risers_sawtooth_stringer_flush_stairs_job_input_params)

    def execute(self):
        # Job execution logic goes here
        pass

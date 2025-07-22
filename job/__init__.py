



from job.straight_closed_risers_sawtooth_stringer_standard_stairs_job import StraightClosedRisersSawtoothStringerStandardStairsJob
from models.job.straight_closed_risers_sawtooth_stringer_standard_stairs_job_params import StraightClosedRisersSawtoothStringerStandardStairsJobInputParams

from job.straight_closed_risers_sawtooth_stringer_flush_stairs_job import StraightClosedRisersSawtoothStringerFlushStairsJob
from models.job.straight_closed_risers_sawtooth_stringer_flush_stairs_job_params import StraightClosedRisersSawtoothStringerFlushStairsJobInputParams



available_job_templates = {
    "StraightClosedRisersSawtoothStringerStandardStairsJobInputParams": {
        "label": "Straight Closed Risers Sawtooth Stringer Standard Stairs",
        "job_class": StraightClosedRisersSawtoothStringerStandardStairsJob,
        "input_params_class": StraightClosedRisersSawtoothStringerStandardStairsJobInputParams
    },
    "StraightClosedRisersSawtoothStringerFlushStairsJobInputParams": {
        "label": "Straight Closed Risers Sawtooth Stringer Flush Stairs",
        "job_class": StraightClosedRisersSawtoothStringerFlushStairsJob,
        "input_params_class": StraightClosedRisersSawtoothStringerFlushStairsJobInputParams
    }
}
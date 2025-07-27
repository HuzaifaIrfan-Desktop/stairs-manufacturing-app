



from job.straight_sawtooth_stringer_standard_stairs_job import StraightSawtoothStringerStandardStairsJob
from models.job.straight_sawtooth_stringer_standard_stairs_job_params import StraightSawtoothStringerStandardStairsJobInputParams

from job.straight_sawtooth_stringer_flush_stairs_job import StraightSawtoothStringerFlushStairsJob
from models.job.straight_sawtooth_stringer_flush_stairs_job_params import StraightSawtoothStringerFlushStairsJobInputParams



available_job_classes = {
    "StraightSawtoothStringerStandardStairsJobInputParams": {
        "label": "Straight Sawtooth Stringer Standard Stairs",
        "job_class": StraightSawtoothStringerStandardStairsJob,
        "input_params_class": StraightSawtoothStringerStandardStairsJobInputParams
    },
    "StraightSawtoothStringerFlushStairsJobInputParams": {
        "label": "Straight Sawtooth Stringer Flush Stairs",
        "job_class": StraightSawtoothStringerFlushStairsJob,
        "input_params_class": StraightSawtoothStringerFlushStairsJobInputParams
    }
}
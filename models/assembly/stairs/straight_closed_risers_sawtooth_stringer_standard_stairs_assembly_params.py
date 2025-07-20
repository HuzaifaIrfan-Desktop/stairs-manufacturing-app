

from pydantic import BaseModel, Field

from models.assembly.assembly_params import AssemblyParams

from models.part.stairs.kicker_params import KickerParams
from models.part.stairs.sawtooth_stringer_params import SawtoothStringerParams
from models.part.stairs.riser_params import RiserParams
from models.part.stairs.tread_params import TreadParams

class StraightClosedRisersSawtoothStringerStandardStairsAssemblyParams(AssemblyParams):
    
    kicker_params: KickerParams = Field(..., description="Parameters for the kicker")
    sawtooth_stringer_params: SawtoothStringerParams = Field(..., description="Parameters for the sawtooth stringer")
    riser_params: RiserParams = Field(..., description="Parameters for the risers")
    tread_params: TreadParams = Field(..., description="Parameters for the treads")
    
    first_riser_params: RiserParams = Field(..., description="Parameters for the first riser")
    last_tread_params: TreadParams = Field(..., description="Parameters for the last tread")
    last_riser_params: RiserParams = Field(..., description="Parameters for the last riser")
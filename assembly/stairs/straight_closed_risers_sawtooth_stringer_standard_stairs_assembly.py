

from assembly.assembly import Assembly
from models.assembly.stairs.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params import StraightClosedRisersSawtoothStringerStandardStairsAssemblyParams

class StraightClosedRisersSawtoothStringerStandardStairsAssembly(Assembly):
    def __init__(self, assembly_params: StraightClosedRisersSawtoothStringerStandardStairsAssemblyParams):
        super().__init__(assembly_params)
        self.kicker_params = assembly_params.kicker_params
        self.sawtooth_stringer_params = assembly_params.sawtooth_stringer_params
        self.riser_params = assembly_params.riser_params
        self.tread_params = assembly_params.tread_params
        
        self.first_riser_params = assembly_params.first_riser_params
        self.last_tread_params = assembly_params.last_tread_params
        self.last_riser_params = assembly_params.last_riser_params

import cadquery as cq
from utils.math import inch_to_mm


from assembly.assembly import Assembly
from models.assembly.stairs.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params import StraightClosedRisersSawtoothStringerStandardStairsAssemblyParams

from part.stairs.kicker import Kicker
from part.stairs.sawtooth_stringer import SawtoothStringer
from part.stairs.riser import Riser
from part.stairs.tread import Tread

class StraightClosedRisersSawtoothStringerStandardStairsAssembly(Assembly):
    def __init__(self, straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params: StraightClosedRisersSawtoothStringerStandardStairsAssemblyParams):

        self.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params=straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params

        self.kicker_params = straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params.kicker_params
        self.sawtooth_stringer_params = straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params.sawtooth_stringer_params
        self.riser_params = straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params.riser_params
        self.tread_params = straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params.tread_params

        self.first_riser_params = straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params.first_riser_params
        self.last_tread_params = straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params.last_tread_params
        self.last_riser_params = straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params.last_riser_params


        super().__init__(straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params)


    def _build(self):
        self.kicker=Kicker(self.kicker_params)
        self.sawtooth_stringer=SawtoothStringer(self.sawtooth_stringer_params)
        self.riser=Riser(self.riser_params)
        self.tread=Tread(self.tread_params)
        self.first_riser=Riser(self.first_riser_params)
        self.last_tread=Tread(self.last_tread_params)
        self.last_riser=Riser(self.last_riser_params)

        self.kicker.export_step()
        self.kicker.export_stl()
        self.kicker.export_dxf_right_view()

        self.sawtooth_stringer.export_step()
        self.sawtooth_stringer.export_stl()
        self.sawtooth_stringer.export_dxf_right_view()

        self.riser.export_step()
        self.riser.export_stl()
        self.riser.export_dxf_right_view()

        self.tread.export_step()
        self.tread.export_stl()
        self.tread.export_dxf_right_view()

        self.first_riser.export_step()
        self.first_riser.export_stl()
        self.first_riser.export_dxf_right_view()

        self.last_tread.export_step()
        self.last_tread.export_stl()
        self.last_tread.export_dxf_right_view()

        self.last_riser.export_step()
        self.last_riser.export_stl()
        self.last_riser.export_dxf_right_view()



    def _assemble(self):
        # Logic to assemble the components based on the parameters
        

        sawtooth_stringer = self.sawtooth_stringer.get().val()
        kicker =  self.kicker.get().val()

        first_riser = self.first_riser.get().val()
        last_tread = self.last_tread.get().val()
        last_riser = self.last_riser.get().val()

        # riser = self.riser.get().val()
        # tread =  self.tread.get().val()


        # box1 = cq.Workplane("XY").box(10, 10, 10).val()
        # box2 = cq.Workplane("XY").box(10, 10, 10).val().translate((15, 0, 0))  # offset after creation

        compound = cq.Compound.makeCompound([sawtooth_stringer, kicker, first_riser, last_tread, last_riser])
        self.cq_assembly = cq.Workplane(obj=compound)


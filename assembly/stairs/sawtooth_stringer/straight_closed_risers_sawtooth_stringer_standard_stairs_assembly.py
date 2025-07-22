
import cadquery as cq
from utils.math import inch_to_mm


from assembly.assembly import Assembly
from models.assembly.stairs.sawtooth_stringer.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params import StraightClosedRisersSawtoothStringerStandardStairsAssemblyParams

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

        self.kicker.export()
        self.riser.export()
        self.tread.export()
        self.first_riser.export()
        self.last_tread.export()
        self.last_riser.export()
        self.sawtooth_stringer.export()

    def _assemble(self):
        # Logic to assemble the components based on the parameters
        
        compound = []

        first_riser = self.first_riser.get().val()
        compound.append(first_riser)
        y_offset = inch_to_mm(self.first_riser_params.riser_thickness)

        if self.kicker_params.kicker_depth > 0 and self.kicker_params.kicker_height > 0 and self.kicker_params.kicker_length > 0:
            kicker =  self.kicker.get().val().translate((0, y_offset, 0))
            compound.append(kicker)

        sawtooth_stringer = self.sawtooth_stringer.get().val().translate((0, y_offset, 0))
        compound.append(sawtooth_stringer)

        second_stringer_x_offset = inch_to_mm(self.tread_params.tread_length) - inch_to_mm(self.sawtooth_stringer_params.stringer_thickness)
        second_sawtooth_stringer = self.sawtooth_stringer.get().val().translate((second_stringer_x_offset, y_offset, 0))
        compound.append(second_sawtooth_stringer)

        z_offset = inch_to_mm(self.sawtooth_stringer_params.first_step_rise_height)


        y_offset = y_offset + inch_to_mm(self.sawtooth_stringer_params.step_run_depth) - inch_to_mm(self.riser_params.riser_thickness)
        tread_y_offset = y_offset - inch_to_mm(self.tread_params.tread_depth)
        tread =  self.tread.get().val().translate((0, tread_y_offset, z_offset))
        compound.append(tread)
        riser = self.riser.get().val().translate((0, y_offset, z_offset))
        compound.append(riser)
        z_offset += inch_to_mm(self.sawtooth_stringer_params.step_rise_height)



        # last_tread = self.last_tread.get().val().translate((0, y_offset, z_offset))
        # last_riser = self.last_riser.get().val().translate((0, y_offset, z_offset))
        # compound.append(last_tread)
        # compound.append(last_riser)

        # box1 = cq.Workplane("XY").box(10, 10, 10).val()
        # box2 = cq.Workplane("XY").box(10, 10, 10).val().translate((15, 0, 0))  # offset after creation

        compound = cq.Compound.makeCompound(compound)
        self.cq_assembly = cq.Workplane(obj=compound)


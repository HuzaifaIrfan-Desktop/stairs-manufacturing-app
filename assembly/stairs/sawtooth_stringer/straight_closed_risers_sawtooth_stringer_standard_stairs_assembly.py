
import cadquery as cq
from utils.math import inch_to_mm


from assembly.assembly import Assembly
from models.assembly.stairs.sawtooth_stringer.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params import StraightClosedRisersSawtoothStringerStandardStairsAssemblyParams

from part.stairs.kicker import Kicker
from part.stairs.sawtooth_stringer import SawtoothStringer
from part.stairs.riser import Riser
from part.stairs.tread import Tread


from models.report.cut_list_params import CutListParams
from report.cut_list_report import CutListReport    

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


        if self.kicker_params.kicker_depth > 0 and self.kicker_params.kicker_height > 0 and self.kicker_params.kicker_length > 0:
            kicker =  self.kicker.get().val().translate((0, inch_to_mm(self.first_riser_params.riser_thickness), 0))
            compound.append(kicker)




        riser_y_offset = self.first_riser_params.riser_thickness -self.riser_params.riser_thickness
        z_offset = self.sawtooth_stringer_params.first_step_rise_height

        for i in range(self.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params.number_of_steps_risers - 2):
            riser_y_offset = riser_y_offset + self.sawtooth_stringer_params.step_run_depth
            tread_y_offset = riser_y_offset - self.tread_params.tread_depth
            tread =  self.tread.get().val().translate((0, inch_to_mm(tread_y_offset), inch_to_mm(z_offset)))
            compound.append(tread)
            riser = self.riser.get().val().translate((0, inch_to_mm(riser_y_offset), inch_to_mm(z_offset)))
            compound.append(riser)
            z_offset += self.sawtooth_stringer_params.step_rise_height

        riser_y_offset = riser_y_offset + self.sawtooth_stringer_params.last_step_run_depth + self.riser_params.riser_thickness - self.last_riser_params.riser_thickness
        tread_y_offset = riser_y_offset - self.last_tread_params.tread_depth



        last_tread = self.last_tread.get().val().translate((0, inch_to_mm(tread_y_offset), inch_to_mm(z_offset)))
        last_riser = self.last_riser.get().val().translate((0, inch_to_mm(riser_y_offset), inch_to_mm(z_offset)))
        compound.append(last_tread)
        compound.append(last_riser)




        # box1 = cq.Workplane("XY").box(10, 10, 10).val()
        # box2 = cq.Workplane("XY").box(10, 10, 10).val().translate((15, 0, 0))  # offset after creation
        stringer_y_offset = self.first_riser_params.riser_thickness
        
        num_of_stringers=self.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params.number_of_stringers
        stairway_width=self.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params.stairway_width
        tread_overhang_side_depth = self.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params.tread_overhang_side_depth
        
        if num_of_stringers == 1:
            stringer_x_offset= stairway_width/2-self.sawtooth_stringer_params.stringer_thickness/2
            sawtooth_stringer = self.sawtooth_stringer.get().val().translate((inch_to_mm(stringer_x_offset),inch_to_mm(stringer_y_offset), 0))
            compound.append(sawtooth_stringer)
        
        if num_of_stringers == 2:

            stringer_x_offset= tread_overhang_side_depth

            sawtooth_stringer = self.sawtooth_stringer.get().val().translate((inch_to_mm(stringer_x_offset),inch_to_mm(stringer_y_offset), 0))
            compound.append(sawtooth_stringer)

            second_stringer_x_offset = self.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params.stairway_width - self.sawtooth_stringer_params.stringer_thickness - tread_overhang_side_depth
            second_sawtooth_stringer = self.sawtooth_stringer.get().val().translate((inch_to_mm(second_stringer_x_offset), inch_to_mm(stringer_y_offset), 0))
            compound.append(second_sawtooth_stringer)

        if num_of_stringers >= 3:

            first_stringer_x_offset= tread_overhang_side_depth

            last__stringer_x_offset = self.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params.stairway_width - self.sawtooth_stringer_params.stringer_thickness - tread_overhang_side_depth


            step = (last__stringer_x_offset - first_stringer_x_offset) / (num_of_stringers - 1)
            x_points=[first_stringer_x_offset + i * step for i in range(num_of_stringers)]
            # print(x_points)

            for stringer_x_offset in x_points:
                sawtooth_stringer = self.sawtooth_stringer.get().val().translate((inch_to_mm(stringer_x_offset), inch_to_mm(stringer_y_offset), 0))
                compound.append(sawtooth_stringer)


        compound = cq.Compound.makeCompound(compound)
        self.cq_assembly = cq.Workplane(obj=compound)



    def export_cut_list(self) -> str:

        cut_list_data=[["Part", "Qty", "Material", "Dimension"]]

        cut_list_data.append( ["Treads", self.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params.number_of_steps_risers-2, self.tread_params.material.material_name, f"{self.tread_params.tread_depth} x {self.tread_params.tread_length}"])
        cut_list_data.append( ["Last Tread", "1", self.last_tread_params.material.material_name, f"{self.last_tread_params.tread_depth} x {self.last_tread_params.tread_length}"])
        cut_list_data.append( ["Risers", self.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params.number_of_steps_risers-2, self.riser_params.material.material_name, f"{self.riser_params.riser_height} x {self.riser_params.riser_length}"])
        cut_list_data.append( ["First Riser", "1", self.first_riser_params.material.material_name, f"{self.first_riser_params.riser_height} x {self.first_riser_params.riser_length}"])
        cut_list_data.append( ["Last Riser", "1", self.last_riser_params.material.material_name, f"{self.last_riser_params.riser_height} x {self.last_riser_params.riser_length}"])
        cut_list_data.append( ["Stringers", self.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params.number_of_stringers, self.sawtooth_stringer_params.material.material_name, self.sawtooth_stringer_params.stringer_length])

        summary_items=[("Total Rise", self.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params.total_rise_height),
                           ("Total Run", self.sawtooth_stringer_params.stringer_total_run),
                           ("Stair Width", self.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params.stairway_width),
                           ("First Riser Height", self.first_riser_params.riser_height),
                           ("Riser Height", self.riser_params.riser_height),
                           ("Last Riser Height", self.last_riser_params.riser_height),
                           ("Run Tread Depth", self.tread_params.tread_depth),
                           ("Last Run Tread Depth", self.last_tread_params.tread_depth),
                           ("Number of Risers", self.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params.number_of_steps_risers),
                           ("Number of Treads", self.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params.number_of_steps_risers - 1),]

        cut_list_params = CutListParams(
            job_name=self.assembly_params.job_name,
            assembly_name=self.assembly_params.assembly_name,
            builder_name=self.assembly_params.builder_name,
            summary_items=summary_items,
            cut_list_data=cut_list_data
        )

        cut_list_report = CutListReport(cut_list_params)
        file_path = cut_list_report.export()

        return file_path
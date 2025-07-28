
import cadquery as cq
from utils.math import inch_to_mm


from assembly.assembly import Assembly
from models.assembly.stairs.sawtooth_stringer.straight_sawtooth_stringer_flush_stairs_assembly_params import StraightSawtoothStringerFlushStairsAssemblyParams

from part.stairs.kicker import Kicker
from part.stairs.sawtooth_stringer import SawtoothStringer
from part.stairs.riser import Riser
from part.stairs.tread import Tread

from models.report.cut_list_params import CutListParams
from report.cut_list_report import CutListReport    

from logger import assembly_logger

class StraightSawtoothStringerFlushStairsAssembly(Assembly):
    def __init__(self, straight_sawtooth_stringer_flush_stairs_assembly_params: StraightSawtoothStringerFlushStairsAssemblyParams):

        self.assembly_params=straight_sawtooth_stringer_flush_stairs_assembly_params

        self.kicker_params = self.assembly_params.kicker_params
        self.sawtooth_stringer_params = self.assembly_params.sawtooth_stringer_params
        self.typical_riser_params = self.assembly_params.typical_riser_params
        self.typical_tread_params = self.assembly_params.typical_tread_params

        self.first_riser_params = self.assembly_params.first_riser_params
        self.last_tread_params = self.assembly_params.last_tread_params



        super().__init__(self.assembly_params)

        


    def _build(self):
        self.kicker=Kicker(self.kicker_params)
        self.sawtooth_stringer=SawtoothStringer(self.sawtooth_stringer_params)
        self.typical_riser=Riser(self.typical_riser_params)
        self.typical_tread=Tread(self.typical_tread_params)
        self.first_riser=Riser(self.first_riser_params)
        self.last_tread=Tread(self.last_tread_params)



    
    def export_parts(self) -> str:

        file_path=""
        
        self.kicker.export()
        self.typical_riser.export()
        self.typical_tread.export()
        self.first_riser.export()
        self.last_tread.export()

        self.sawtooth_stringer.export()


        return file_path

    def export_cam(self) -> str:
        self.sawtooth_stringer.export_cam()


    def export_drawings(self) -> str:
        # Placeholder for drawing export logic
        file_path = ""

        file_path = self.export_dxf_right_view()
        self.export_drawing_from_dxf(file_path, text_scale=4.0)

        four_steps_assembly_params=self.assembly_params.model_copy()
        four_steps_assembly_params.total_opening_rise_height*=(4/self.assembly_params.number_of_steps)
        four_steps_assembly_params.assembly_name = f"four_steps_{self.assembly_params.assembly_name}"
        four_steps_assembly_params.number_of_steps=4
        four_steps_assembly_params.compute()
        four_steps_assembly_params.sawtooth_stringer_params.part_name = f"four_steps_{self.sawtooth_stringer_params.part_name}"
        
        # four_steps_assembly_params.sawtooth_stringer_params.number_of_stringer_rise=4
        four_steps_assembly = StraightSawtoothStringerFlushStairsAssembly(four_steps_assembly_params)
        four_steps_assembly_dxf_file_path=four_steps_assembly.export_dxf_right_view()
        four_steps_assembly.export_drawing_from_dxf(four_steps_assembly_dxf_file_path, text_scale=4.0)
        four_steps_assembly_stringer_dxf_file_path=four_steps_assembly.sawtooth_stringer.export_dxf_right_view()
        four_steps_assembly.sawtooth_stringer.export_drawing_from_dxf(four_steps_assembly_stringer_dxf_file_path, text_scale=4.0)


        self.kicker.export_drawings()
        self.typical_riser.export_drawings()
        self.typical_tread.export_drawings()
        self.first_riser.export_drawings()
        self.last_tread.export_drawings()
        self.sawtooth_stringer.export_drawings()

        return file_path
    
    def _assemble(self):
        # Logic to assemble the components based on the parameters
        
        compound = []

        if not self.assembly_params.open_riser:
            first_riser = self.first_riser.get().val()
            compound.append(first_riser)
            y_offset_first_riser_thickness =self.first_riser_params.riser_thickness
        else:
            y_offset_first_riser_thickness = 0


        if self.kicker_params.kicker_depth > 0 and self.kicker_params.kicker_height > 0 and self.kicker_params.kicker_length > 0:
            kicker =  self.kicker.get().val().translate((0, inch_to_mm(y_offset_first_riser_thickness), 0))
            compound.append(kicker)



        riser_y_offset = y_offset_first_riser_thickness -self.typical_riser_params.riser_thickness
        z_offset = self.sawtooth_stringer_params.first_stringer_rise_height

        for i in range(self.assembly_params.number_of_steps - 1):
            riser_y_offset = riser_y_offset + self.sawtooth_stringer_params.typical_stringer_run_depth
            tread_y_offset = riser_y_offset - self.typical_tread_params.tread_depth

            if not self.assembly_params.open_riser:
                typical_tread =  self.typical_tread.get().val().translate((0, inch_to_mm(tread_y_offset), inch_to_mm(z_offset)))
                compound.append(typical_tread)
                typical_riser = self.typical_riser.get().val().translate((0, inch_to_mm(riser_y_offset), inch_to_mm(z_offset)))
                compound.append(typical_riser)
            else:
                tread_y_offset = tread_y_offset + self.typical_riser_params.riser_thickness
                typical_tread =  self.typical_tread.get().val().translate((0, inch_to_mm(tread_y_offset), inch_to_mm(z_offset)))
                compound.append(typical_tread)



            z_offset += self.sawtooth_stringer_params.typical_stringer_rise_height


        riser_y_offset = riser_y_offset + self.sawtooth_stringer_params.last_stringer_run_depth + self.typical_riser_params.riser_thickness
        tread_y_offset = riser_y_offset - self.last_tread_params.tread_depth
        last_tread = self.last_tread.get().val().translate((0, inch_to_mm(tread_y_offset), inch_to_mm(z_offset)))

        compound.append(last_tread)


        # box1 = cq.Workplane("XY").box(10, 10, 10).val()
        # box2 = cq.Workplane("XY").box(10, 10, 10).val().translate((15, 0, 0))  # offset after creation


        stringer_y_offset = y_offset_first_riser_thickness
        
        num_of_stringers=self.assembly_params.number_of_stringers
        stairway_width=self.assembly_params.stairway_width
        tread_overhang_side_depth = self.assembly_params.tread_overhang_side_depth
        
        if num_of_stringers == 1:
            stringer_x_offset= stairway_width/2-self.sawtooth_stringer_params.stringer_thickness/2
            sawtooth_stringer = self.sawtooth_stringer.get().val().translate((inch_to_mm(stringer_x_offset),inch_to_mm(stringer_y_offset), 0))
            compound.append(sawtooth_stringer)
        
        if num_of_stringers == 2:

            stringer_x_offset= tread_overhang_side_depth

            sawtooth_stringer = self.sawtooth_stringer.get().val().translate((inch_to_mm(stringer_x_offset),inch_to_mm(stringer_y_offset), 0))
            compound.append(sawtooth_stringer)

            second_stringer_x_offset = self.assembly_params.stairway_width - self.sawtooth_stringer_params.stringer_thickness - tread_overhang_side_depth
            second_sawtooth_stringer = self.sawtooth_stringer.get().val().translate((inch_to_mm(second_stringer_x_offset), inch_to_mm(stringer_y_offset), 0))
            compound.append(second_sawtooth_stringer)

        if num_of_stringers >= 3:

            first_stringer_x_offset= tread_overhang_side_depth

            last__stringer_x_offset = self.assembly_params.stairway_width - self.sawtooth_stringer_params.stringer_thickness - tread_overhang_side_depth


            step = (last__stringer_x_offset - first_stringer_x_offset) / (num_of_stringers - 1)
            x_points=[first_stringer_x_offset + i * step for i in range(num_of_stringers)]
            # print(x_points)

            for stringer_x_offset in x_points:
                sawtooth_stringer = self.sawtooth_stringer.get().val().translate((inch_to_mm(stringer_x_offset), inch_to_mm(stringer_y_offset), 0))
                compound.append(sawtooth_stringer)


        compound = cq.Compound.makeCompound(compound)
        self.cq_assembly = cq.Workplane(obj=compound)




    def export_reports(self) -> str:
        return self.export_cut_list()
    
    
    def export_cut_list(self) -> str:

        cut_list_data=[["Part", "Qty", "Material", "Dimension"]]

        cut_list_data.append( ["Typical Treads", self.assembly_params.number_of_steps-1, self.typical_tread_params.tread_material.material_name, f"{self.typical_tread_params.tread_depth} x {self.typical_tread_params.tread_length}"])
        cut_list_data.append( ["Last Tread", "1", self.last_tread_params.tread_material.material_name, f"{self.last_tread_params.tread_depth} x {self.last_tread_params.tread_length}"])
        if not self.assembly_params.open_riser:
            # closed Riser assembly add riser parts in list
            cut_list_data.append( ["Typical Risers", self.assembly_params.number_of_steps-1, self.typical_riser_params.riser_material.material_name, f"{self.typical_riser_params.riser_height} x {self.typical_riser_params.riser_length}"])
            cut_list_data.append( ["First Riser", "1", self.first_riser_params.riser_material.material_name, f"{self.first_riser_params.riser_height} x {self.first_riser_params.riser_length}"])
        cut_list_data.append( ["Stringers", self.assembly_params.number_of_stringers, self.sawtooth_stringer_params.stringer_material.material_name, self.sawtooth_stringer_params.stringer_length])

        summary_items=[("Total Rise", self.assembly_params.total_assembly_rise_height),
                           ("Total Run", self.assembly_params.total_assembly_run_depth),
                           ("Stair Width", self.assembly_params.stairway_width),
                           ("First Riser Height", self.first_riser_params.riser_height),
                           ("Typical Riser Height", self.typical_riser_params.riser_height),
                           ("Typical Run Tread Depth", self.typical_tread_params.tread_depth),
                           ("Last Run Tread Depth", self.last_tread_params.tread_depth),
                           ("Number of Risers", self.assembly_params.number_of_steps),
                           ("Number of Treads", self.assembly_params.number_of_steps),]

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
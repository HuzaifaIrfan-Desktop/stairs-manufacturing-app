
import cadquery as cq
from utils.math import inch_to_mm


from assembly.assembly import Assembly
from models.assembly.u_stairs.u_standard_stairs_assembly_params import UStandardStairsAssemblyParams
from assembly.stairs.sawtooth_stringer.straight_sawtooth_stringer_standard_stairs_assembly import StraightSawtoothStringerStandardStairsAssembly
from part.landing.u_landing import ULanding

from part.stairs.kicker import Kicker
from part.stairs.sawtooth_stringer import SawtoothStringer
from part.stairs.riser import Riser
from part.stairs.tread import Tread

from models.report.cut_list_params import CutListParams
from report.cut_list_report import CutListReport    

from logger import assembly_logger

class UStandardStairsAssembly(Assembly):
    def __init__(self, u_standard_stairs_assembly_params: UStandardStairsAssemblyParams):

        self.assembly_params=u_standard_stairs_assembly_params


        self.u_landing_params = self.assembly_params.u_landing_params
        self.upper_standard_stairs_assembly_params = self.assembly_params.upper_standard_stairs_assembly_params
        self.lower_standard_stairs_assembly_params = self.assembly_params.lower_standard_stairs_assembly_params



        super().__init__(self.assembly_params)

        


    def _build(self):
        self.u_landing=ULanding(self.u_landing_params)
        self.upper_standard_stairs_assembly=StraightSawtoothStringerStandardStairsAssembly(self.upper_standard_stairs_assembly_params)
        self.lower_standard_stairs_assembly=StraightSawtoothStringerStandardStairsAssembly(self.lower_standard_stairs_assembly_params)




    
    def export_parts(self) -> str:

        file_path=""
        
        self.u_landing.export()
        self.upper_standard_stairs_assembly.export()
        self.lower_standard_stairs_assembly.export()


        return file_path



    def export_drawings(self) -> str:
        # Placeholder for drawing export logic
        file_path = ""

        file_path = self.export_dxf_right_view()
        self.export_drawing_from_dxf(file_path, text_scale=4.0)
        file_path = self.export_dxf_top_view()
        self.export_drawing_from_dxf(file_path, text_scale=4.0)
        
        self.u_landing.export_drawings()
        self.upper_standard_stairs_assembly.export_drawings()
        self.lower_standard_stairs_assembly.export_drawings()

        return file_path


    def export_cam(self) -> str:

        # Placeholder for CAM export logic
        file_path = ""
        self.upper_standard_stairs_assembly.export_cam()
        self.lower_standard_stairs_assembly.export_cam()

        return file_path

    def _assemble(self):
        # Logic to assemble the components based on the parameters
        
        compound = []



        upper_stairs_assembly = self.upper_standard_stairs_assembly.get().val()
        upper_stairs_assembly = upper_stairs_assembly.rotate((0, 0, 0), (0, 0, 1), 180)
        upper_stairs_x_position = self.assembly_params.stairway_width 
        upper_stairs_y_position = self.upper_standard_stairs_assembly_params.total_assembly_run_depth
        upper_stairs_z_position = self.u_landing_params.landing_top_position

        upper_stairs_assembly = upper_stairs_assembly.translate((inch_to_mm(upper_stairs_x_position), inch_to_mm(upper_stairs_y_position), inch_to_mm(upper_stairs_z_position)))

        compound.append(upper_stairs_assembly)


        lower_stairs_assembly = self.lower_standard_stairs_assembly.get().val()
        lower_stairs_x_position = self.assembly_params.stairway_width + self.assembly_params.center_wall_thickness
        lower_stairs_y_position = self.u_landing_params.landing_y_position - self.lower_standard_stairs_assembly_params.total_assembly_run_depth
        lower_stairs_z_position = 0
        lower_stairs_assembly = lower_stairs_assembly.translate((inch_to_mm(lower_stairs_x_position), inch_to_mm(lower_stairs_y_position), inch_to_mm(lower_stairs_z_position)))
        compound.append(lower_stairs_assembly)






        compound.append(self.u_landing.get().val())

        compound = cq.Compound.makeCompound(compound)
        self.cq_assembly = cq.Workplane(obj=compound)



    def export_reports(self) -> str:
        self.upper_standard_stairs_assembly.export_reports()
        self.lower_standard_stairs_assembly.export_reports()


        # return self.export_cut_list()

        return ""
    

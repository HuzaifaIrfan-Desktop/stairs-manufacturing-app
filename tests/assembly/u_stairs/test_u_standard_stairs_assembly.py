

from assembly.u_stairs.u_standard_stairs_assembly import UStandardStairsAssembly

from models.assembly.u_stairs.u_standard_stairs_assembly_params import UStandardStairsAssemblyParams   

from models.part.stairs.kicker_params import KickerParams
from models.part.stairs.sawtooth_stringer_params import SawtoothStringerParams
from models.part.stairs.riser_params import RiserParams
from models.part.stairs.tread_params import TreadParams

from models.material.plywood import plywood_1

def test_u_standard_stairs_assembly():

    job_name = "test_u_stairs_job"


    # Create assembly parameters
    assembly_params = UStandardStairsAssemblyParams(
        job_name=job_name,
        assembly_name="test_u_standard_stairs_assembly",
        builder_name="Test Builder",

        total_opening_rise_height=136.0,
        opening_length=128.5,
        opening_width=96.0,
        tread_depth=11.0,

        center_wall_thickness=3.5,

        number_of_upper_steps=10,
        number_of_lower_steps=10,

    )

    assembly = UStandardStairsAssembly(assembly_params)


    assert assembly is not None
    assert assembly.get() is not None
    assert assembly.get_assembly_params() is not None
    assert assembly.export_assembly_params() is not None
    assert assembly.export_step() is not None
    assert assembly.export_stl() is not None
    assert assembly.export_dxf_top_view() is not None
    assert assembly.export_dxf_front_view() is not None
    assert assembly.export_dxf_right_view() is not None

    assert assembly.export_reports() is not None

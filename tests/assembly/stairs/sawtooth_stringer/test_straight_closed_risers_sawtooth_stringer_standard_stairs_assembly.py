

from assembly.stairs.sawtooth_stringer.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly import StraightClosedRisersSawtoothStringerStandardStairsAssembly

from models.assembly.stairs.sawtooth_stringer.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params import StraightClosedRisersSawtoothStringerStandardStairsAssemblyParams   

from models.part.stairs.kicker_params import KickerParams
from models.part.stairs.sawtooth_stringer_params import SawtoothStringerParams
from models.part.stairs.riser_params import RiserParams
from models.part.stairs.tread_params import TreadParams

from models.material.plywood import plywood_1

def test_straight_closed_risers_sawtooth_stringer_standard_stairs_assembly():

    job_name = "test_sawtooth_stairs_job"


    # Create assembly parameters
    assembly_params = StraightClosedRisersSawtoothStringerStandardStairsAssemblyParams(
        job_name=job_name,
        assembly_name="test_straight_closed_risers_sawtooth_stringer_standard_stairs_assembly",
        builder_name="Test Builder",
        # total_assembly_rise_height= 122.0,
        stairway_width= 36.75,
        number_of_steps=16,

        first_riser_height=6.63,
        last_riser_hanger_height=13.25,
        last_tread_depth=11.5,
        typical_riser_height=7.63,
        typical_tread_depth=11.5,


        tread_overhang_nosing_depth=1.0,
        tread_overhang_side_depth=1.0,

        number_of_stringers=4,


        # first_riser_material=plywood_1

    )

    assembly = StraightClosedRisersSawtoothStringerStandardStairsAssembly(assembly_params)


    assert assembly is not None
    assert assembly.get() is not None
    assert assembly.get_assembly_params() is not None
    assert assembly.export_assembly_params() is not None
    assert assembly.export_step() is not None
    assert assembly.export_stl() is not None
    # assert assembly.export_dxf_top_view() is not None
    # assert assembly.export_dxf_front_view() is not None
    assert assembly.export_dxf_right_view() is not None
    assert assembly.export_cut_list() is not None
    
    # assert assembly.export_parts() is not None
    # assert assembly.export_drawing() is not None
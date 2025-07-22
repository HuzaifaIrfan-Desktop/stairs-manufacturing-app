

from assembly.stairs.sawtooth_stringer.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly import StraightClosedRisersSawtoothStringerStandardStairsAssembly

from models.assembly.stairs.sawtooth_stringer.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params import StraightClosedRisersSawtoothStringerStandardStairsAssemblyParams   

from models.part.stairs.kicker_params import KickerParams
from models.part.stairs.sawtooth_stringer_params import SawtoothStringerParams
from models.part.stairs.riser_params import RiserParams
from models.part.stairs.tread_params import TreadParams




def test_straight_closed_risers_sawtooth_stringer_standard_stairs_assembly():

    job_name = "test_assembly_job"


    # Create assembly parameters
    assembly_params = StraightClosedRisersSawtoothStringerStandardStairsAssemblyParams(
        job_name=job_name,
        assembly_name="test_straight_closed_risers_sawtooth_stringer_standard_stairs_assembly"
    )

    assembly = StraightClosedRisersSawtoothStringerStandardStairsAssembly(assembly_params)

    assert assembly is not None
    assert assembly.get() is not None
    assert assembly.get_assembly_params() is not None
    assert assembly.export_assembly_params() is not None
    assert assembly.export_step() is not None
    assert assembly.export_stl() is not None
    assert assembly.export_dxf_top_view() is not None
    assert assembly.export_dxf_front_view() is not None
    assert assembly.export_dxf_right_view() is not None
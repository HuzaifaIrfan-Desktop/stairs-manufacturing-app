

from assembly.stairs.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly import StraightClosedRisersSawtoothStringerStandardStairsAssembly

from models.assembly.stairs.straight_closed_risers_sawtooth_stringer_standard_stairs_assembly_params import StraightClosedRisersSawtoothStringerStandardStairsAssemblyParams   

from models.part.stairs.kicker_params import KickerParams
from models.part.stairs.sawtooth_stringer_params import SawtoothStringerParams
from models.part.stairs.riser_params import RiserParams
from models.part.stairs.tread_params import TreadParams




def test_straight_closed_risers_sawtooth_stringer_standard_stairs_assembly():

    job_name = "test_assembly_job"

    kicker_params = KickerParams(
        job_name=job_name,
        part_name="test_kicker",
        kicker_height=4,
        kicker_depth=1,
        kicker_length=36
    )

    sawtooth_stringer_params = SawtoothStringerParams(
        job_name=job_name,
        part_name="test_sawtooth_stringer",
        stringer_width=12,
        stringer_thickness=1,

        stringer_length=36,

        first_step_rise_height=7,
        last_step_run_depth=10,

        step_rise_height=7,
        step_run_depth=10,

        number_of_stringer_rise=12,
        number_of_stringer_run=12,

        angle_of_stringer=30,
        stringer_placement_from_top=5,




    )


    riser_params = RiserParams(
        job_name=job_name,
        part_name="test_riser",
        riser_height=7,
        riser_thickness=1,
        riser_length=36
    )

    tread_params = TreadParams(
        job_name=job_name,
        part_name="test_tread",
        tread_depth=10,
        tread_thickness=1,
        tread_length=36
    )

    first_riser_params = RiserParams(
        job_name=job_name,
        part_name="test_first_riser",
        riser_height=7,
        riser_thickness=1,
        riser_length=36
    )
    last_tread_params = TreadParams(
        job_name=job_name,
        part_name="test_last_tread",
        tread_depth=10,
        tread_thickness=1,
        tread_length=36
    )

    last_riser_params = RiserParams(
        job_name=job_name,
        part_name="test_last_riser",
        riser_height=7,
        riser_thickness=1,
        riser_length=36
    )

    # Create assembly parameters
    assembly_params = StraightClosedRisersSawtoothStringerStandardStairsAssemblyParams(
        job_name=job_name,
        assembly_name="test_straight_closed_risers_sawtooth_stringer_standard_stairs_assembly",
        kicker_params=kicker_params,
        sawtooth_stringer_params=sawtooth_stringer_params,
        riser_params=riser_params,
        tread_params=tread_params,
        first_riser_params=first_riser_params,
        last_tread_params=last_tread_params,
        last_riser_params=last_riser_params
    )

    assembly = StraightClosedRisersSawtoothStringerStandardStairsAssembly(assembly_params)

    assert assembly is not None
    assert assembly.get() is not None
    assert assembly.export_step() is not None
    assert assembly.export_stl() is not None
    assert assembly.export_dxf_top_view() is not None
    assert assembly.export_dxf_front_view() is not None
    assert assembly.export_dxf_right_view() is not None

from part.stairs import sawtooth_stringer
from models.part.stairs.sawtooth_stringer_params import SawtoothStringerParams



def test_sawtooth_stringer_build():
    stringer_params = SawtoothStringerParams(job_name="test_job", part_name="test_sawtooth_stringer",
                                              first_step_rise_height=6.63, last_step_run_depth=11.5,
                                              step_rise_height=7.63, step_run_depth=11.5,
                                              number_of_stringer_run=12,
                                              
                                              kicker_height=1.0, kicker_depth=1.0)
    stringer = sawtooth_stringer.SawtoothStringer(stringer_params)
    cq_part = stringer.get()
    assert cq_part is not None
    assert cq_part.val().Volume() > 0  # Ensure the part has a non-zero volume

def test_sawtooth_stringer_export():
    stringer_params = SawtoothStringerParams(job_name="test_job", part_name="test_sawtooth_stringer",
                                              first_step_rise_height=6.63, last_step_run_depth=11.5,
                                              step_rise_height=7.63, step_run_depth=11.5,number_of_stringer_run=15,
                                              )
    stringer = sawtooth_stringer.SawtoothStringer(stringer_params)

    stringer.export_part_params()

    # Test STEP export
    stringer.export_step()

    # Test STL export
    stringer.export_stl()

    # Test DXF export
    stringer.export_dxf_right_view()

    stringer.export_cam()

    stringer.export_drawing()

    # Check if files are created (this is a simple check, in real tests you might want to check file existence)
    assert True  # Placeholder for actual file existence checks

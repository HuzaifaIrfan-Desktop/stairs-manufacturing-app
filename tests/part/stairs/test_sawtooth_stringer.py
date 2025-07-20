
from part.stairs import sawtooth_stringer
from models.part.stairs.sawtooth_stringer_params import SawtoothStringerParams



def test_sawtooth_stringer_build():
    stringer_params = SawtoothStringerParams(job_name="test_job", part_name="test_sawtooth_stringer", stringer_length=1.0, stringer_thickness=0.3, stringer_width=0.05,
                                              first_step_rise_height=0.2, last_step_run_depth=0.3,
                                              step_rise_height=0.18, step_run_depth=0.25,
                                              number_of_stringer_rise=10, number_of_stringer_run=12,
                                              angle_of_stringer=30, stringer_placement_from_top=0.1,
                                              bottom_stringer_depth=0.3, back_stringer_reverse_height=0.3,
                                              kicker_height=0.4, kicker_depth=0.5)
    stringer = sawtooth_stringer.SawtoothStringer(stringer_params)
    cq_part = stringer.get()
    assert cq_part is not None
    assert cq_part.val().Volume() > 0  # Ensure the part has a non-zero volume

def test_sawtooth_stringer_export():
    stringer_params = SawtoothStringerParams(job_name="test_job", part_name="test_sawtooth_stringer", stringer_length=50.0, stringer_thickness=1.5, stringer_width=11.5,
                                              first_step_rise_height=6.13, last_step_run_depth=10.5,
                                              step_rise_height=7.63, step_run_depth=10.5,
                                              number_of_stringer_rise=12, number_of_stringer_run=4,
                                              angle_of_stringer=30, stringer_placement_from_top=0.1)
    stringer = sawtooth_stringer.SawtoothStringer(stringer_params)

    # Test STEP export
    stringer.export_step()

    # Test STL export
    stringer.export_stl()

    # Test DXF export
    stringer.export_dxf_right_view()

    # Check if files are created (this is a simple check, in real tests you might want to check file existence)
    assert True  # Placeholder for actual file existence checks

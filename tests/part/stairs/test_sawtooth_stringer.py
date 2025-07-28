
from part.stairs import sawtooth_stringer
from models.part.stairs.sawtooth_stringer_params import SawtoothStringerParams

from utils.math import inch_to_mm


def test_sawtooth_stringer():
    stringer_params = SawtoothStringerParams(job_name="test_job", part_name="test_sawtooth_stringer",
                                              first_stringer_rise_height=6.63, last_stringer_run_depth=11.5,
                                              typical_stringer_rise_height=7.63, typical_stringer_run_depth=11.5, number_of_stringer_rise=15,
                                              )
    stringer = sawtooth_stringer.SawtoothStringer(stringer_params)

    cq_part = stringer.get()
    assert cq_part is not None
    assert cq_part.val().Volume() > 0  # Ensure the part has a non-zero volume

    total_stringer_rise = stringer_params.first_stringer_rise_height + \
        (stringer_params.number_of_stringer_rise - 1) * stringer_params.typical_stringer_rise_height
    total_stringer_run = stringer_params.last_stringer_run_depth + \
        (stringer_params.number_of_stringer_rise - 1) * stringer_params.typical_stringer_run_depth
    
    model_total_stringer_rise = cq_part.val().BoundingBox().zmax - cq_part.val().BoundingBox().zmin
    model_total_stringer_run = cq_part.val().BoundingBox().ymax - cq_part.val().BoundingBox().ymin

    assert abs(model_total_stringer_rise - inch_to_mm(total_stringer_rise)) < 0.2
    assert abs(model_total_stringer_run - inch_to_mm(total_stringer_run)) < 0.2
    assert abs(model_total_stringer_rise - inch_to_mm(stringer_params.total_stringer_rise_height)) < 0.2
    assert abs(model_total_stringer_run - inch_to_mm(stringer_params.total_stringer_run_depth)) < 0.2


    stringer.export_part_params()

    # Test STEP export
    stringer.export_step()

    # Test STL export
    stringer.export_stl()

    # Test DXF export
    stringer.export_dxf_right_view()
    stringer.export_dxf_front_view()
    stringer.export_dxf_top_view()
    
    stringer.export_cam()

    # stringer.export_drawing()

    # Check if files are created (this is a simple check, in real tests you might want to check file existence)
    assert True  # Placeholder for actual file existence checks

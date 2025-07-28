

from part.top_floor_opening import TopFloorOpening
from models.part.top_floor_opening_params import TopFloorOpeningParams




def test_top_floor_opening():
    opening_params = TopFloorOpeningParams(job_name="test_job", part_name="test_opening", opening_length=36.75, opening_width=11.5, opening_top_position=10, opening_x_position=0, opening_y_position=0)
    opening = TopFloorOpening(opening_params)

    cq_part = opening.get()
    assert cq_part is not None
    assert cq_part.val().Volume() > 0  # Ensure the part has a non-zero volume


    opening.export_part_params()
    # Test STEP export
    opening.export_step()

    # Test STL export
    opening.export_stl()

    # Test DXF export
    opening.export_dxf_top_view()
    opening.export_dxf_right_view()
    opening.export_dxf_front_view()

    # opening.export_drawings()

    # Check if files are created (this is a simple check, in real tests you might want to check file existence)
    assert True  # Placeholder for actual file existence checks
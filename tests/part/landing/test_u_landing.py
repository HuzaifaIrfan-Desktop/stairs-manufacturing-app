

from part.landing.u_landing import ULanding
from models.part.landing.u_landing_params import ULandingParams




def test_u_landing():
    u_landing_params = ULandingParams(job_name="test_job", part_name="test_u_landing", landing_length=96, landing_width=48.5, stairway_width=46.25, upper_stairway_placement_overhang=3, landing_top_position=68, landing_x_position=0, landing_y_position=0, right_hand_turn=False)
    u_landing = ULanding(u_landing_params)

    cq_part = u_landing.get()
    assert cq_part is not None
    assert cq_part.val().Volume() > 0  # Ensure the part has a non-zero volume


    u_landing.export_part_params()
    # Test STEP export
    u_landing.export_step()

    # Test STL export
    u_landing.export_stl()


    # Test DXF export
    u_landing.export_dxf_top_view()
    u_landing.export_dxf_right_view()

    # u_landing.export_drawing()

    # Check if files are created (this is a simple check, in real tests you might want to check file existence)
    assert True  # Placeholder for actual file existence checks
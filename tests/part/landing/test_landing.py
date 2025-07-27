

from part.landing.landing import Landing
from models.part.landing.landing_params import LandingParams




def test_landing():
    landing_params = LandingParams(job_name="test_job", part_name="test_landing", landing_length=36.75, landing_width=11.5, landing_top_position=10, landing_x_position=0, landing_y_position=0)
    landing = Landing(landing_params)

    cq_part = landing.get()
    assert cq_part is not None
    assert cq_part.val().Volume() > 0  # Ensure the part has a non-zero volume


    landing.export_part_params()
    # Test STEP export
    landing.export_step()

    # Test STL export
    landing.export_stl()


    # Test DXF export
    landing.export_dxf_top_view()
    landing.export_dxf_right_view()

    # landing.export_drawing()

    # Check if files are created (this is a simple check, in real tests you might want to check file existence)
    assert True  # Placeholder for actual file existence checks
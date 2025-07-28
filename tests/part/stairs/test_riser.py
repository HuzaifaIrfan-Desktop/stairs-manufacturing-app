

from part.stairs import kicker, riser
from part.stairs.riser import Riser
from models.part.stairs.riser_params import RiserParams


def test_riser():
    riser_params = RiserParams(job_name="test_job", part_name="test_riser", riser_length=36.75, riser_height=7.625)
    riser = Riser(riser_params)

    cq_part = riser.get()
    assert cq_part is not None
    assert cq_part.val().Volume() > 0 

    riser.export_part_params()

    # Test STEP export
    riser.export_step()

    # Test STL export
    riser.export_stl()

    # Test DXF export
    riser.export_dxf_right_view()
    riser.export_dxf_front_view()
    riser.export_dxf_top_view()

    # riser.export_drawing()

    # Check if files are created (this is a simple check, in real tests you might want to check file existence)
    assert True  # Placeholder for actual file existence checks
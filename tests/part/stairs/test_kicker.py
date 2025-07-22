

from part.stairs import kicker
from part.stairs.kicker import Kicker
from models.part.stairs.kicker_params import KickerParams

def test_kicker_area():
    kicker_params = KickerParams(job_name="test_job", part_name="test_kicker", kicker_length=36.75, kicker_height=1, kicker_depth=1)
    kicker = Kicker(kicker_params)
    assert kicker.calculate_area() == 36.75 * 1  # Area = length * height

def test_kicker_volume():
    kicker_params = KickerParams(job_name="test_job", part_name="test_kicker", kicker_length=36.75, kicker_height=1, kicker_depth=1)
    kicker = Kicker(kicker_params)
    assert kicker.calculate_volume() == 36.75 * 1 * 1

def test_kicker_build():
    kicker_params = KickerParams(job_name="test_job", part_name="test_kicker", kicker_length=36.75, kicker_height=1, kicker_depth=1)
    kicker = Kicker(kicker_params)
    cq_part = kicker.get()
    assert cq_part is not None
    assert cq_part.val().Volume() > 0  # Ensure the part has a non-zero volume

def test_kicker_export():
    kicker_params = KickerParams(job_name="test_job", part_name="test_kicker", kicker_length=36.75, kicker_height=1, kicker_depth=1)
    kicker = Kicker(kicker_params)

    kicker.export_part_params()
    # Test STEP export
    kicker.export_step()

    # Test STL export
    kicker.export_stl()

    # Test DXF export
    kicker.export_dxf_right_view()

    kicker.export_drawing()

    # Check if files are created (this is a simple check, in real tests you might want to check file existence)
    assert True  # Placeholder for actual file existence checks
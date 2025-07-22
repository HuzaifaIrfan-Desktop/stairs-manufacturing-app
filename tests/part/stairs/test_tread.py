

from part.stairs import kicker
from part.stairs.tread import Tread
from models.part.stairs.tread_params import TreadParams

def test_tread_area():
    tread_params = TreadParams(job_name="test_job", part_name="test_tread", tread_length=36.75, tread_depth=11.5)
    tread = Tread(tread_params)
    assert tread.calculate_area() == 36.75 * 11.5

def test_tread_volume():
    tread_params = TreadParams(job_name="test_job", part_name="test_tread", tread_length=36.75, tread_depth=11.5)
    tread = Tread(tread_params)
    assert tread.calculate_volume() == 36.75 * 11.5 * 1

def test_tread_build():
    tread_params = TreadParams(job_name="test_job", part_name="test_tread", tread_length=36.75, tread_depth=11.5)
    tread = Tread(tread_params)
    cq_part = tread.get()
    assert cq_part is not None
    assert cq_part.val().Volume() > 0  # Ensure the part has a non-zero volume

def test_tread_export():
    tread_params = TreadParams(job_name="test_job", part_name="test_tread", tread_length=36.75, tread_depth=11.5)
    tread = Tread(tread_params)
    
    tread.export_part_params()
    # Test STEP export
    tread.export_step()
    
    # Test STL export
    tread.export_stl()

    # Test DXF export
    tread.export_dxf_right_view()

    tread.export_drawing()

    # Check if files are created (this is a simple check, in real tests you might want to check file existence)
    assert True  # Placeholder for actual file existence checks
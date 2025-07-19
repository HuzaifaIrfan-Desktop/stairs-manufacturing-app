

from part.stairs.tread import Tread
from models.part.stairs.tread_params import TreadParams

def test_tread_area():
    tread_params = TreadParams(job_name="test_job", part_name="test_tread", tread_length=1.0, tread_depth=0.3, tread_thickness=0.05)
    tread = Tread(tread_params)
    assert tread.calculate_area() == 0.3

def test_tread_volume():
    tread_params = TreadParams(job_name="test_job", part_name="test_tread", tread_length=1.0, tread_depth=0.3, tread_thickness=0.05)
    print(tread_params)
    tread = Tread(tread_params)
    assert tread.calculate_volume() == 0.015

def test_tread_build():
    tread_params = TreadParams(job_name="test_job", part_name="test_tread", tread_length=1.0, tread_depth=0.3, tread_thickness=0.05)
    tread = Tread(tread_params)
    cq_part = tread.get()
    assert cq_part is not None
    assert cq_part.val().Volume() > 0  # Ensure the part has a non-zero volume

def test_tread_export():
    tread_params = TreadParams(job_name="test_job", part_name="test_tread", tread_length=1.0, tread_depth=0.3, tread_thickness=0.05)
    tread = Tread(tread_params)
    
    # Test STEP export
    tread._export_step()
    
    # Test STL export
    tread._export_stl()
    
    # Test DXF export
    tread._export_dxf()
    
    # Check if files are created (this is a simple check, in real tests you might want to check file existence)
    assert True  # Placeholder for actual file existence checks
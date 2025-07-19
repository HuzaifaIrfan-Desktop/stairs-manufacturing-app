import cadquery as cq

# Create a simple example part
result = (
    cq.Workplane("XY")
    .box(10, 20, 5)  # Base box
    .faces(">Z")
    .workplane()
    .circle(3)
    .extrude(10)  # Cylinder on top
    .edges("|Z")
    .fillet(1)  # Fillet vertical edges
)

# Export to different formats
# 1. Export to STEP (Standard for CAD exchange)
cq.exporters.export(result, 'output/example_part.step', 'STEP')

# 2. Export to STL (For 3D printing)
cq.exporters.export(result, 'output/example_part.stl', 'STL')

# 3. Export to DXF (For 2D drawings)
# First we need to get a 2D projection for DXF
top_view = result.faces(">Z").wires()  # Get top view wires
cq.exporters.export(top_view, 'output/example_top_view.dxf', 'DXF')

# Show in CQ-Editor (if running there)
# show_object(result, name="example_part")
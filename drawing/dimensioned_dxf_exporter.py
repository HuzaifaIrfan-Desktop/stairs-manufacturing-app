

import os
from turtle import st
import ezdxf
from ezdxf.units import IN, MM

from ezdxf.math import Vec2

from ezdxf.addons.drawing import Frontend, RenderContext, pymupdf, layout, config

from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy
from ezdxf.addons.drawing.properties import Properties

import pathlib

from utils.math import inch_to_mm, mm_to_inch

class DimensionedDXFExporter:
    def __init__(self, dxf_file_path:str, text_scale: float = 1.0):
        self.file_path = dxf_file_path
        self.output_dir = f"{pathlib.Path(self.file_path).parent}/drawings"
        self.file_stem = pathlib.Path(self.file_path).stem
        self.doc = ezdxf.new('R2018', setup=True)
        self.msp = self.doc.modelspace()
        self.doc.units = IN

        self.text_scale = text_scale

        print(f"DimensionedDXFExporter initialized with {self.file_path}")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.read()  # Read existing DXF if it exists

        # self.build()

    def read(self):
        dxf_file_path = self.file_path
        if os.path.exists(dxf_file_path):
            self.doc = ezdxf.readfile(dxf_file_path)
            self.msp = self.doc.modelspace()
            self.doc.units = IN
        else:
            raise FileNotFoundError(f"DXF file not found: {dxf_file_path}")
        
        # list blocks in the DXF file
        blocks = self.doc.blocks
        print("Blocks in the DXF file:")
        for block_name in blocks:
            print(f" - {block_name}")

        # list entities in the modelspace
        entities = self.msp.query('*')
        print("Entities in the modelspace:")
        for entity in entities:
            print(f" - {entity.dxftype()} at {entity.dxf.insert if hasattr(entity.dxf, 'insert') else 'N/A'}")
        # list layers in the DXF file
        layers = self.doc.layers
        print("Layers in the DXF file:")
        for layer in layers:
            print(f" - {layer}: color={layer.color}")

        #list all LINEs in the DXF file
        lines = self.msp.query('LINE')
        print("Lines in the modelspace:")
        for line in lines:
            start = line.dxf.start
            end = line.dxf.end
            print(f" - LINE from {start} to {end}")
        
        # add dimensions to lines
        for line in lines:
            start = Vec2(line.dxf.start)
            end = Vec2(line.dxf.end)
            # Calculate dimension line offset
            direction = end - start
            if direction.magnitude == 0:
                print(f"Skipping dimension for zero-length line from {start} to {end}")
                continue
            offset_dir = direction.orthogonal().normalize() 
            dim_line_pos = (start + end) * 0.5 + offset_dir

            dimension_value= f'{mm_to_inch((end - start).magnitude)}"'
            print(f"Adding dimension from {start} to {end} at {dim_line_pos} with value {dimension_value}")

            # Add the dimension
            dim = self.msp.add_linear_dim(
                base=dim_line_pos,  # Location of dimension line
                p1=start,           # Start point of measured entity
                p2=end,             # End point of measured entity
                dimstyle='Standard',
                text=dimension_value,
                override={
                    'dimtxt': 5.0*self.text_scale, # Text height (default is 2.5)
                    'dimgap': 5.0*self.text_scale,
                    'dimdle': 5.0*self.text_scale,
                    'dimasz': 5.0*self.text_scale,  # Arrow size (default is 2.5)
                    'dimblk': '',    # Use simple arrowheads instead of blocks
                    'dimexo': 5.0*self.text_scale,  # Extension line offset (default is 1.25)
                    # Extension line extension (default is 1.25)
                    "dimdec": 2,  # Number of decimal places
                    "dimtix": 1,  # Force user text (suppresses measurement)
                    "dimtad": 1,  # Text above dimension line
                    "dimjust": 0, # Horizontal justification (0=centered)
                    "dimclrd": 0, # Dimension line color (0=BYBLOCK)
                    "dimclre": 0, # Extension line color (0=BYBLOCK)
                    "dimclrt": 0, # Text color (0=BYBLOCK)
                    "dimse1": 0,  # Suppress first extension line (0=off)
                    "dimse2": 0,  # Suppress second extension line (0=off)
                    "dimsoxd": 0, # Suppress outside dimension lines (0=off)
                    "dimtofl": 1, # Force line inside extension lines (1=on)
                    "dimtoh": 0,  # Text outside horizontal (0=off)
                    "dimtsz": 0,  # Tick size (0=arrowheads)
                    "dimlfac": 1.0, # Scale factor for dimension measurement   # Conversion factor from mm to inches
                    "dimpost": '<>"',
                },
                angle=direction.angle_deg
            ) 
            
            dim.render()


    def export(self)-> tuple[str, str]:

        pdf_file_path = f"{self.output_dir}/{self.file_stem}.pdf"
        png_file_path = f"{self.output_dir}/{self.file_stem}.png"

        msp = self.doc.modelspace()
        # 1. create the render context
        context = RenderContext(self.doc)
        # 2. create the backend
        backend = pymupdf.PyMuPdfBackend()
        # 3. create and configure the frontend
        # 1. Create configuration with proper settings
        
        cfg = Configuration(
            background_policy=BackgroundPolicy.WHITE,
            line_policy=config.LinePolicy.SOLID,
            color_policy=config.ColorPolicy.BLACK,  # Force black for all elements
            min_lineweight=0.2,  # Increase if lines are still missing
            max_flattening_distance=0.01,  # For better curve rendering
        )

        frontend = Frontend(context, backend, config=cfg)
        # 4. draw the modelspace
        frontend.draw_layout(msp)

        page = layout.Page(11, 8.5, layout.Units.inch)
        # 6. get the PDF rendering as bytes
        pdf_bytes = backend.get_pdf_bytes(page)
        with open(pdf_file_path, "wb") as fp:
            fp.write(pdf_bytes)

        # 6. get the PNG rendering as bytes
        png_bytes = backend.get_pixmap_bytes(page, fmt="png", dpi=300)
        with open(png_file_path, "wb") as fp:
            fp.write(png_bytes)

        print(f"PDF and PNG exported successfully to {self.output_dir}")

        return pdf_file_path, png_file_path



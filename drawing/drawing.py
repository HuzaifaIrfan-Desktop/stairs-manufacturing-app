
import pathlib
from drawing.dimensioned_dxf_exporter import DimensionedDXFExporter

from PIL import Image
import io


import svgwrite
import cairosvg
from lxml import etree
import os
from pathlib import Path
import datetime
import fitz  # PyMuPDF
from models.drawing.drawing_params import DrawingParams

from logger import drawing_logger

class Drawing:
    def __init__(self, job_name:str, part_name:str, dxf_file_path:str, text_scale:float):
        self.job_name = job_name
        self.part_name = part_name
        self.dxf_file_path = dxf_file_path
        self.text_scale = text_scale
        
        self.drawing_params= DrawingParams(
            job_name=self.job_name,
            drawing_name=f"{self.part_name}"
        )

        self.dimensioned_pdf_file_path, self.dimensioned_png_file_path = DimensionedDXFExporter(self.drawing_params,dxf_file_path, text_scale=text_scale).export()

        self.output_dir = os.path.join(os.getcwd(), f'output/{self.drawing_params.job_name}/drawings')
        self.file_stem = pathlib.Path(self.dimensioned_png_file_path).stem #self.part_name 

        self.template_svg_file_path = os.path.join(os.getcwd(), "drawing_templates", "ANSIA_Landscape.svg")
        self.template_pdf_file_path = f'{self.output_dir}/template/{self.file_stem}.pdf'
        os.makedirs(os.path.dirname(self.template_pdf_file_path), exist_ok=True)
        self.drawing_pdf_file_path = f'{self.output_dir}/drawing_{self.file_stem}.pdf'

        drawing_logger.info(f"Initialized Drawing with job_name: {self.job_name}, part_name: {self.part_name}, dxf_file_path: {self.dxf_file_path}, text_scale: {self.text_scale}")


    def edit_and_export_template(self):
        # Parse the existing SVG
        tree = etree.parse(self.template_svg_file_path)
        root = tree.getroot()
        
        # Example edit: Change all text elements to uppercase
        ns = {'svg': 'http://www.w3.org/2000/svg'}
        for text_elem in root.findall('.//svg:tspan', ns):
            # print(f"Editing text: {text_elem.text}")

            if text_elem.text == "Drawing Title 1":
                text_elem.text = f"{self.part_name}"
            elif text_elem.text == "Drawing Title 2":
                text_elem.text = f"{self.job_name}"
            elif text_elem.text == "Drawing Title 3":
                text_elem.text = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            if text_elem.text:
                text_elem.text = text_elem.text.upper()

        # Ensure the 'tmp' directory exists
        os.makedirs('tmp', exist_ok=True)
        # Save edited SVG temporarily
        
        temp_svg = 'tmp/edited.svg'
        tree.write(temp_svg)
        
        # Convert to PDF
        cairosvg.svg2pdf(url=temp_svg, write_to=self.template_pdf_file_path)

        # print(f"Edited SVG saved as PDF: {self.template_pdf_file_path}")


    def scale_embed_png_to_template(self):
        
        # Scale and embed PNG in center of template PDF, output to drawing PDF


        # Open the template PDF
        template_pdf = fitz.open(self.template_pdf_file_path)
        page = template_pdf[0]

        # Load the PNG image
        img_rect = fitz.Rect(0, 0, 0, 0)
        img = fitz.open(self.dimensioned_png_file_path)
        img_page = img[0]
        img_pix = img_page.get_pixmap()
        img_width = img_pix.width
        img_height = img_pix.height

        # Get page size
        page_width = page.rect.width
        page_height = page.rect.height

        # Scale image to fit within page, preserving aspect ratio
        scale = min(page_width / img_width, page_height / img_height) * 0.6  # 70% of page
        new_width = img_width * scale
        new_height = img_height * scale 

        # Center image on page
        # x0 = (page_width - new_width) / 2
        # y0 = (page_height - new_height) / 2

        x0 = 100
        y0 = 50
        x1 = x0 + new_width
        y1 = y0 + new_height
        img_rect = fitz.Rect(x0, y0, x1, y1)

        # Insert image
        # page.insert_image(img_rect, filename=self.dimensioned_png_file_path) # this insert high size raw image
        
        # Convert PNG to JPEG in memory
        png = Image.open(self.dimensioned_png_file_path).convert("RGB")
        jpeg_io = io.BytesIO()
        png.save(jpeg_io, format="JPEG", quality=70)
        jpeg_bytes = jpeg_io.getvalue()

        # Use in PyMuPDF
        page.insert_image(img_rect, stream=jpeg_bytes)

                
        
        # Insert text annotation at the center of the image
        # text = f"{self.part_name} - {self.job_name}"
        # text_x = x0 + (new_width / 2)
        # text_y = y0 + (new_height / 2) -100
        # page.insert_text(
        #     fitz.Point(text_x, text_y),
        #     text,
        #     fontsize=24,
        #     color=(0, 0, 0),
        # )

        # Save to output PDF
        template_pdf.save(self.drawing_pdf_file_path)
        # print(f"Embedded PNG into PDF and saved to: {self.drawing_pdf_file_path}")


    def export(self) -> str:
        self.edit_and_export_template()
        self.scale_embed_png_to_template()

        drawing_logger.info(f"Exported drawing to PDF: {self.drawing_pdf_file_path}")

        return self.drawing_pdf_file_path
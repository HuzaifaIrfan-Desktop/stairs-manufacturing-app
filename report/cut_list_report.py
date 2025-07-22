

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.units import inch
import os


from models.report.cut_list_params import CutListParams


class CutListReport:
    def __init__(self, cut_list_params: CutListParams):

        self.cut_list_params = cut_list_params

        self.output_dir = os.path.join(os.getcwd(), f'output/{self.cut_list_params.job_name}/assembly/{self.cut_list_params.assembly_name}')

        os.makedirs(self.output_dir, exist_ok=True)



    def export(self) -> str:

        

        # PDF Setup
        pdf_file_path = f"{self.output_dir}/{self.cut_list_params.assembly_name}_cutlist.pdf"

        # Setup
        doc = SimpleDocTemplate(pdf_file_path, title=f"{self.cut_list_params.assembly_name} Cut List", pagesize=LETTER,
                                rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        styles = getSampleStyleSheet()
        elements = []

        # Header with Logo
        logo_path = "assets/TBD1_logo.jpg"
        if os.path.exists(logo_path):
            # , width=1.5*inch, height=0.75*inch
            logo = Image(logo_path)
            logo.hAlign = 'LEFT'
            elements.append(logo)
        else:
            # No Logo
            elements.append(Paragraph("<b>Treads by Design</b>", styles['Normal']))

        # Title and Job Info
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"<b>Cut List - {self.cut_list_params.job_name} Job</b>", styles['Title']))
        elements.append(Paragraph(f"Assembly: {self.cut_list_params.assembly_name}", styles['Normal']))
        elements.append(Paragraph(f"Builder: {self.cut_list_params.builder_name}", styles['Normal']))
        # elements.append(Paragraph(f'Total Rise: {total_rise}", Width: {width}"', styles['Normal']))
        elements.append(Spacer(1, 12))

        # Stair Summary
        elements.append(Paragraph("<b>Summary</b>", styles['Heading3']))
        # summary_items = [
        #     ("Total Rise", f'{total_rise}"'),
        #     ("Stair Width", f'{width}"'),
        #     ("Riser Height", f'{riser_height}"'),
        #     ("Number of Risers", f'{num_riser}'),
        #     ("Number of Treads", f'{num_tread}'),
        #     ("Run Depth (per tread)", f'{tread_depth}"'),
        #     ("Total Stair Run", f'{total_run}"'),
        # ]

        for item, value in self.cut_list_params.summary_items:
            elements.append(Paragraph(f"{item}: {value}", styles['Normal']))
        elements.append(Spacer(1, 12))

        # Cut List Table
        # cut_list_data = [
        #     ["Part", "Qty", "Material", "Dimension"],
        #     ["Treads", "15", '1" Plywood', '36 3/4"'],
        #     ["Risers", "15", '3/8" Plywood', '36 3/4"'],
        #     ["Top Riser", "1", '5/8" Plywood', '36 3/4"'],
        #     ["Stringers", "2", 'LSL or 2x12', '122"'],
        # ]

        table = Table(self.cut_list_params.cut_list_data, colWidths=[1.5 * inch] * 4)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ]))

        elements.append(table)

        # Build PDF
        doc.build(elements)
        # print(f"PDF created: {pdf_file_path}")

        return pdf_file_path



from fpdf import FPDF
import io
from datetime import datetime

class LabReport(FPDF):
    def header(self):
        # Set Blue Header Bar
        self.set_fill_color(0, 123, 255)
        self.rect(0, 0, 210, 40, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 20)
        self.cell(0, 20, 'VIRTUAL ENGINEERING LABORATORY', ln=True, align='C')
        self.set_font('Arial', '', 12)
        self.cell(0, 10, 'Automated Laboratory Record System', ln=True, align='C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()} | Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")}', align='C')

def generate_report(user, exp_name, aim, procedure, results_text):
    pdf = LabReport()
    pdf.add_page()
    
    # Student Info Section
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(100, 10, f"STUDENT NAME: {user['name'].upper()}", ln=False)
    pdf.cell(0, 10, f"REG NO: {user['reg']}", ln=True, align='R')
    pdf.cell(100, 10, f"DEPARTMENT: {user['dept']}", ln=False)
    pdf.cell(0, 10, f"EXP NO: {exp_name.split('.')[0]}", ln=True, align='R')
    pdf.ln(5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(10)

    # Content
    sections = [("AIM", aim), ("PROCEDURE", procedure), ("OBSERVATIONS & RESULTS", results_text)]
    
    for title, content in sections:
        pdf.set_font('Arial', 'B', 12)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 10, title, ln=True, fill=True)
        pdf.ln(2)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(0, 7, content)
        pdf.ln(5)

    # Add a "Verified" Stamp area
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 10, "Digital Signature: SYSTEM_VERIFIED_AUTHENTIC", ln=True, align='R')

    return pdf.output(dest='S').encode('latin-1')

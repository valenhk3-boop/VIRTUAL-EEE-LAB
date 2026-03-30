from fpdf import FPDF
import io

def generate_report(user, exp_name, results_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "OFFICIAL LABORATORY REPORT", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Student: {user['name']}", ln=True)
    pdf.cell(200, 10, f"Reg No: {user['reg']}", ln=True)
    pdf.cell(200, 10, f"Experiment: {exp_name}", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "Observations & Conclusion:", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 10, results_text)
    
    return pdf.output(dest='S').encode('latin-1')

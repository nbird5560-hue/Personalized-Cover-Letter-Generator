from pick import pick
from fpdf import FPDF
from pathlib import Path
# Import Document from python-docx
from docx import Document
from docx.shared import Inches
import re

def choose_output_type(text, role, company):
    # Added '.docx' to the picking options
    options = ['.docx', '.pdf', '.txt', 'at terminal']
    selected, index = pick(options, "Pick output type: ")
    
    # Defining and safely creating the output directory
    output_dir = Path("./outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    def clean_filename(path: str):
        return re.sub(r'[^a-zA-Z0-9_. -]', '', path).strip('.-')
        
    # Constructing clean paths using pathlib
    base_filename = clean_filename(f"{company} - {role} - Cover Letter")

    pdf_path = output_dir / f"{base_filename}.pdf"
    docx_path = output_dir / f"{base_filename}.docx"
    txt_path = output_dir / f"{base_filename}.txt"
    


    def handle_case(index):
        match index:

            case 0: # .docx
                doc = Document()                
                for section in doc.sections:
                    section.top_margin = Inches(0.7)
                    section.bottom_margin = Inches(0.7)
                    section.left_margin = Inches(0.75)
                    section.right_margin = Inches(0.75)                
                doc.add_paragraph(text)                
                doc.save(str(docx_path))
                print(f"DOCX Generated at: {docx_path}")

            case 1: # .pdf
                pdf = FPDF(format="Letter")
                pdf.set_margins(top=17.78, bottom=17.78, left=19.05, right=19.05)
                pdf.add_page()
                pdf.set_font("Helvetica", size=11)
                pdf.multi_cell(w=0, h=5, txt=text)
                
                pdf.output(str(pdf_path))
                print(f"PDF Generated at: {pdf_path}")
                
            case 2: # .txt
                with open(txt_path, mode="w", encoding="utf-8") as f:
                    f.write(text)
                print(f"TXT generated at: {txt_path}")
                
            case 3: # at terminal
                print(text)
    
    handle_case(index=index)
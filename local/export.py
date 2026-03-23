import os
import time
import re
from fpdf import FPDF
from docx import Document
from docx.shared import Pt

def ensure_outputs():
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

def save_result(text: str, mode: str):
    ensure_outputs()
    fname = f"outputs/result_{mode}_{int(time.time())}.txt"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(text)
    return fname

def save_as_pdf(text: str):
    ensure_outputs()
    pdf = FPDF()
    pdf.add_page()
    # Make sure you have the font or use a standard one
    pdf.set_font("Arial", size=11) 
    clean_text = re.sub(r'[#*`]', '', text)
    for line in clean_text.split('\n'):
        pdf.multi_cell(0, 8, line.strip())
    fname = f"outputs/analysis_{int(time.time())}.pdf"
    pdf.output(fname)
    return fname

def save_as_docx(text: str):
    ensure_outputs()
    doc = Document()
    for line in text.split('\n'):
        doc.add_paragraph(line.strip())
    fname = f"outputs/analysis_{int(time.time())}.docx"
    doc.save(fname)
    return fname
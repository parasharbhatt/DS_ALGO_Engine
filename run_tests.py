import os
import sys
import io
import unittest
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def execute_suite_and_export_pdf():
    # 1. Establish isolated testing runtime directories
    os.makedirs("test_outputs", exist_ok=True)
    
    # 2. Capture terminal standard streams dynamically 
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    loader = unittest.TestLoader()
    
    print("Executing automated test suite suite...")
    suite = loader.discover(start_dir="tests", pattern="test_*.py")
    result = runner.run(suite)
    
    # Extract structural console logs
    stream.seek(0)
    test_logs = stream.read()
    
    # 3. Create Datetime Output Stamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"test_outputs/test_run_{timestamp}.pdf"
    
    # 4. Initialize PDF Compilation Pipeline via ReportLab
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    # Custom Palette Styling
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=22, textColor='#0284c7', spaceAfter=15)
    meta_style = ParagraphStyle('MetaStyle', parent=styles['Normal'], fontSize=10, textColor='#475569', spaceAfter=20)
    summary_style = ParagraphStyle('SummaryStyle', parent=styles['Normal'], fontSize=12, spaceAfter=15, leading=16)
    log_box_style = ParagraphStyle('LogStyle', parent=styles['Code'], fontSize=9, textColor='#0f172a', backColor='#f8fafc', borderColor='#cbd5e1', borderWidth=1, padding=12)

    # Document Layout Components Assembler
    story = []
    story.append(Paragraph("DSA Automation Engine — Verification Report", title_style))
    story.append(Paragraph(f"<b>Execution Date/Time:</b> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/><b>Target Environment:</b> Local VS Code Virtual Workspace", meta_style))
    
    # Map high-level boolean outcomes safely
    outcome_text = "<b>STATUS:</b> <font color='#16a34a'><b>PASSED</b></font>" if result.wasSuccessful() else "<b>STATUS:</b> <font color='#dc2626'><b>FAILED</b></font>"
    story.append(Paragraph(f"{outcome_text}<br/><b>Tests Executed:</b> {result.testsRun} | <b>Failures:</b> {len(result.failures)} | <b>Errors:</b> {len(result.errors)}", summary_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("<b>Raw Terminal Stream Traces:</b>", styles['Heading3']))
    story.append(Spacer(1, 5))
    story.append(Preformatted(test_logs, log_box_style))
    
    # Build the file on disk
    doc.build(story)
    print(f"Test Run Artifact compiled successfully: {pdf_filename}")

if __name__ == "__main__":
    execute_suite_and_export_pdf()

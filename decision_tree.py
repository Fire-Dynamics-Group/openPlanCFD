from pathlib import Path
from docxtpl import DocxTemplate


document_name = 'Event Tree.docx'
document_path = Path(__file__).parent /"Report Template"/"Event Tree.docx"
doc = DocxTemplate(document_path)

def fill_event_tree(output_filename=Path(__file__).parent /"Report Template"/'test output report.docx'):
    PASS1_PD = 78
    PASS2_PD = 78
    FAIL1_PD = 100 - PASS1_PD
    FAIL2_PD = 100 - PASS2_PD

    context = {
        "PASS1_PD": PASS1_PD,
        "PASS2_PD": PASS2_PD,
        "FAIL1_PD": FAIL1_PD,
        "FAIL2_PD": FAIL2_PD,
    }

    doc.render(context)

    doc.save(output_filename)    


fill_event_tree()
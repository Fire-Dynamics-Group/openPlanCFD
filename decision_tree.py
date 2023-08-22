from pathlib import Path
from docxtpl import DocxTemplate
'''
# TODO: drop in text here
is contained over multiple storeys{% endif %} 
features open kitchens when the area of the apartment exceeds 8m x 4m, 
a floor area greater than 12m x 16m.

'''

# document_name = 'Event Tree.docx'
document_path = Path(__file__).parent /"Report Template"/"Template_Open_Plan_Report.docx"
# Report Template\Template_Open_Plan_Report.docx
doc = DocxTemplate(document_path)
# c:\Users\IanShaw\Fire Dynamics Group Dropbox\Thomas O'Driscoll\R&D\NHBC 8x10_1000x1000.json
def input_report_variables(
                            has_area_above_12x16,
                            has_kitchen_above_8x4,
                            is_multi_storey, 
                            num_kitchens, 
                            output_filename=Path(__file__).parent /"Report Template"/'test output report2.docx'
                            ):
    PASS1_PD = 78
    PASS2_PD = 78
    FAIL1_PD = 100 - PASS1_PD
    FAIL2_PD = 100 - PASS2_PD

    ''' REASONS_FOR_STUDY variable logic '''
    is_multi_storey_text = 'is contained over multiple storeys'
    if num_kitchens > 1:
        singular_article_kitchen = ''
        plural_kitchens = 's'
    else:
        singular_article_kitchen = 'an '
        plural_kitchens = ''
    has_kitchen_above_8x4_text = f'features {singular_article_kitchen}open kitchen{plural_kitchens} where the area of the apartment exceeds 8m x 4m'
    has_area_above_12x16_text = f'a floor area greater than 12m x 16m'

    reasons_for_study_text_list = []
    reasons_for_study_text = ''
    # if x add text for x to list
    if is_multi_storey:
        reasons_for_study_text_list.append(is_multi_storey_text)
    if has_kitchen_above_8x4:
        reasons_for_study_text_list.append(has_kitchen_above_8x4_text)
    if has_area_above_12x16:
        reasons_for_study_text_list.append(has_area_above_12x16_text)
    # add and between last two
    if len(reasons_for_study_text_list) > 1:
        reasons_for_study_text = 'and ' + reasons_for_study_text_list[-1]
         # and comma between others
        if len(reasons_for_study_text_list) > 2:
            reasons_for_study_text = ', '.join(reasons_for_study_text_list[:-1]) + " " + reasons_for_study_text
    else:
        reasons_for_study_text = reasons_for_study_text_list[0]

    context = {
        # "PASS1_PD": PASS1_PD,
        # "PASS2_PD": PASS2_PD,
        # "FAIL1_PD": FAIL1_PD,
        # "FAIL2_PD": FAIL2_PD,
        "ONE_STOREY": True,
        "AUTHOR_ NAME": "Test Author",
        "CLIENT_NAME": "Test Client",
        "TODAYS_DATE": "Test Date",
        "PROJECT_NAME": "Test Project",
        "REASONS_FOR_STUDY": reasons_for_study_text
    }

    doc.render(context)

    doc.save(output_filename)    


input_report_variables(
                            has_area_above_12x16=True,
                            has_kitchen_above_8x4=True,
                            is_multi_storey=True, 
                            num_kitchens=1    
)
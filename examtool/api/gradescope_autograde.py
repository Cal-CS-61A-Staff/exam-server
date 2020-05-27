import examtool.api.download
from examtool.api.gradescope_upload import APIClient
import os

def generate_and_upload_exams_and_setup_outline(gs_client, email, password, gs_class_id, gs_title, exam, out, name_question_id, sid_question_id, compact=False):
    if not gs_client.logged_in:
        gs_client.log_in(email, password)
    out = out or "out/export/" + exam
    template_questions, email_to_data_map, total = examtool.api.download.download(exam)
    examtool.api.download.export(template_questions, email_to_data_map, total, exam, out, name_question_id, sid_question_id, compact)
    outline_path = f"{out}/OUTLINE.pdf"
    assignment_id = gs_client.create_exam(gs_class_id, gs_title, outline_path)
    if not assignment_id:
        print("Failed to create the exam! Make sure it has a unique title.")
        return

    client = APIClient()
    client.log_in(email, password)

    for file_name in os.listdir(out):
        if "@" not in file_name:
            continue
        student_email = file_name[:-4]
        client.upload_submission(gs_class_id, assignment_id, student_email, os.path.join(out, file_name))
    
    return (template_questions, email_to_data_map, assignment_id)

def grade_assignment():
    pass
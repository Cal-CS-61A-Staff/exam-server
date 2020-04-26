import csv
import json

import click
from cryptography.fernet import Fernet
from google.cloud import firestore
from google.cloud.exceptions import NotFound


@click.command()
@click.option("--name", prompt=True, default="cs61a-test-final")
@click.option("--exam", prompt=True, default="sample_exam.json", type=click.File('r'))
@click.option("--roster", prompt=True, default="sample_roster.csv", type=click.File('r'))
@click.option("--default-deadline", prompt=True, default=0, type=int)
def upload_exam(name, exam, roster, default_deadline):
    exam = exam.read()
    roster = csv.reader(roster, delimiter=',')

    db = firestore.Client()
    ref = db.collection("exams").document(name)
    exam = json.loads(exam)

    exam["default_deadline"] = default_deadline
    exam["secret"] = Fernet.generate_key()

    try:
        exam["secret"] = ref.get().to_dict()["secret"]
    except (NotFound, TypeError):
        pass

    ref.set(exam)

    ref = db.collection("roster").document(name).collection("deadline")
    next(roster)  # ditch headers
    batch = db.batch()
    cnt = 0
    for email, deadline in roster:
        doc_ref = ref.document(email)
        batch.set(doc_ref, {"deadline": int(deadline)})
        cnt += 1
        if cnt > 400:
            batch.commit()
            batch = db.batch()
            cnt = 0
            print("Batch of 400 writes complete")
    batch.commit()

    ref = db.collection("exams").document("all")
    data = ref.get().to_dict()
    if name not in data["exam-list"]:
        data["exam-list"].append(name)
    ref.set(data)

    print("Exam uploaded with password:", exam["secret"][:-1].decode("utf-8"))


if __name__ == '__main__':
    upload_exam()

import os
import pathlib
from io import BytesIO
from json import load

import click
from pikepdf import Pdf

from examtool.api.convert import convert
from examtool.api.scramble import scramble as scramble_fn
from examtool.api.database import get_exam
from examtool.api.gen_latex import render_latex
from examtool.cli.utils import exam_name_option, hidden_output_folder_option, prettify


@click.command()
@exam_name_option
@click.option(
    "--json",
    default=None,
    type=click.File("r"),
    help="The exam JSON you wish to compile. Leave blank to compile the deployed exam.",
)
@click.option(
    "--md",
    default=None,
    type=click.File("r"),
    help="The exam Markdown you wish to compile. Leave blank to compile the deployed exam.",
)
@click.option(
    "--scramble",
    default=None,
    help="Scrambles the exam based off of the email seed."
)
@click.option(
    "--keep_data",
    default=False,
    is_flag=True,
    help="Scrambe keep data flag."
)
@hidden_output_folder_option
def compile(exam, json, md, scramble, keep_data, out):
    """
    Compile one PDF, unencrypted.
    Exam must have been deployed first.
    """
    if not out:
        out = ""

    pathlib.Path(out).mkdir(parents=True, exist_ok=True)

    if json:
        print("Loading exam...")
        exam_data = load(json)
    elif md:
        print("Compiling exam...")
        exam_text_data = md.read()
        exam_data = convert(exam_text_data)
    else:
        print("Fetching exam...")
        exam_data = get_exam(exam=exam)

    if scramble:
        print("Scrambling exam...")
        exam_data = scramble_fn(scramble, exam_data, keep_data=keep_data)

    print("Rendering exam...")
    with render_latex(
        exam_data, {"coursecode": prettify(exam.split("-")[0]), "description": "Sample Exam."}
    ) as pdf:
        pdf = Pdf.open(BytesIO(pdf))
        pdf.save(os.path.join(out, exam + ".pdf"))
        pdf.close()


if __name__ == "__main__":
    compile()

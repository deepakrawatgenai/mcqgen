import os
import PyPDF2
import json
import traceback
from src.mcqgenerator.logger import logging


def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader= PyPDF2.PdfReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
        except Exception as e:
            raise Exception("Error Reading the PDF file.")
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        raise Exception("Unsupported file format, only PDF and txt file supported.")
    
def get_table_data(quiz_str):
    try:
        logging.info(type(quiz_str))
        quiz_dict= json.loads(quiz_str)
        quiz_table_data=[]
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " | ".join(
                [
                    f"{option}: {option_value}"
                    for option, option_value in value["options"].items()
                    ]
                )
            correct = value["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})
        logging.info(type(quiz_table_data))
        return quiz_table_data
    except Exception as e:
        traceback.print_exception(type(e),e,e.__traceback__)
        return False
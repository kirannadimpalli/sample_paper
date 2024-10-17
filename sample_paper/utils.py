import re
import PyPDF2
import vertexai
import os
import json
from PyPDF2 import PdfReader
from vertexai.generative_models import GenerativeModel, Part
from google.auth import load_credentials_from_file
from dotenv import load_dotenv


load_dotenv()
google_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
project_id = os.getenv("PROJECT_ID")

vertexai.init(project=project_id, location="us-central1")
model = GenerativeModel("gemini-1.5-flash-002")
credentials_path = google_credentials
credentials = load_credentials_from_file(credentials_path)

def extract_pdf_content(pdf_stream):
    """Extract text content from a PDF file."""
    reader = PdfReader(pdf_stream)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text



# def extract_pdf_data(pdf_content: str) -> dict:
#     prompt = f"""
#     I have the following raw text extracted from a PDF. Can you format it into a structured JSON format that includes sections, questions, and metadata?

#     Raw PDF text:
#     {pdf_content}

#     Please format it as a JSON structure with the following fields:
#     - title: The title of the paper (str)
#     - type: The type of paper (e.g., "previous_year") (str)
#     - time: Total time for the paper (integer)
#     - marks: Total marks for the paper (int)
#     - params: Metadata such as board, grade, and subject (dict)
#     - sections: Each section contains multiple questions (list of section)
#     - Each question has fields like question (str), answer (str), type (str), reference ID (str), and hint (str), question_slug (str), params (str).
#     If no property is not found in given pdf, make an default value for that key eg: type = '', or time = 0 or sections = [] etc
#     """
#     response = model.generate_content(prompt)
#     formatted_response = format_gemini_response(response)

#     return formatted_response


def format_gemini_response(response):
    if hasattr(response, 'candidates'):
        text = response.candidates[0].content.parts[0].text
    else:
        print("Response does not have the expected structure.")
        return None

    match = re.search(r'```json\n(.*?)\n```', text, re.DOTALL)
    
    if match:
        json_str = match.group(1)
        try:
            formatted_json = json.loads(json_str)
            return formatted_json
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            return None
    else:
        print("No JSON found in the response.")
        return None



def extract_pdf_data(pdf_content: str) -> dict:
    json_response = {
            "title": "The Sample Paper Title",
            "type": "previous_year",
            "time": 180,
            "marks": 100,
            "params": {
                "board": "CBSE",
                "grade": 10,
                "subject": "Mathematics"
            },
            "sections": [
                {
                    "name": "Section 1",
                    "marks_per_question": 5,
                    "question_type": "default",
                    "questions": [
                        {
                            "question_text": "Solve the quadratic equation: x² + 5x + 6 = 0",
                            "answer": "The solutions are x = -2 and x = -3.",
                            "hint": "Use the quadratic formula or factorization method.",
                            "reference_id": "QE001"
                        },
                        {
                            "question_text": "In a right-angled triangle, if one angle is 30°, what is the other acute angle?",
                            "answer": "The other acute angle is 60°.",
                            "hint": "Remember that the sum of angles in a triangle is 180°.",
                            "reference_id": "GT001"
                        }
                    ]
                }
            ]
        }
    return json_response
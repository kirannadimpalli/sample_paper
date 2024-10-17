import asyncio

def extract_pdf_data(pdf_content: str) -> dict:
    """Mock function to simulate extracting PDF data and formatting it to JSON."""
    # await asyncio.sleep(5)  # Simulating async operation (e.g., processing with Vertex AI)
    
    # Mock response (normally this would be extracted from the PDF)
    sample_paper_json = {
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
    return sample_paper_json

from PyPDF2 import PdfReader

def extract_pdf_content(pdf_stream):
    """Extract text content from a PDF file."""
    reader = PdfReader(pdf_stream)  # pdf_stream is now a file-like object
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
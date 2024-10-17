from pydantic import BaseModel, ValidationError
from typing import List, Optional
import json

# Define the Pydantic models
class Question(BaseModel):
    question_text: str
    answer: str
    type: Optional[str] = None
    question_slug: Optional[str] = None
    reference_id: str
    hint: Optional[str] = None
    params: dict = {}

class Section(BaseModel):
    name: str
    marks_per_question: int
    question_type: Optional[str] = None
    questions: List[Question]

class SamplePaper(BaseModel):
    title: str
    type: str
    time: int
    marks: int
    params: dict
    tags: List[str] = []
    chapters: List[str] = []
    sections: List[Section]

# The provided JSON response (formatted for clarity)
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

# Simulating missing fields that should be present in a valid response
json_response["tags"] = []  # Adding missing tags
json_response["chapters"] = []  # Adding missing chapters

# Validate the data using the Pydantic model
try:
    paper = SamplePaper(**json_response)
    breakpoint()
    print(paper.json(indent=2))  # Output the formatted JSON
    # Return a 200 response (simulated)
    print("200 OK: Validation successful.")
except ValidationError as e:
    print("Validation Error:", e)

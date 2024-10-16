from pydantic import BaseModel
from typing import List, Optional

class Question(BaseModel):
    question: str
    answer: str
    type: str
    question_slug: str
    reference_id: str
    hint: Optional[str] = None
    params: dict = {}

class Section(BaseModel):
    marks_per_question: int
    type: str
    questions: List[Question]

class SamplePaper(BaseModel):
    title: str
    type: str
    time: int
    marks: int
    params: dict
    tags: List[str]
    chapters: List[str]
    sections: List[Section]

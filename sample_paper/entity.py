from pydantic import BaseModel
from typing import List, Optional

class Question(BaseModel):
    question: str
    answer: str
    type: Optional[str] = None
    question_slug: Optional[str] = None
    reference_id: str
    hint: Optional[str] = None
    params: dict = {}

class Section(BaseModel):
    marks_per_question: int
    type: Optional[str] = None
    questions: List[Question]

class SamplePaper(BaseModel):
    title: str
    type: str
    time: int
    marks: int
    params: dict
    tags: List[str]
    chapters: List[str] = []
    sections: List[Section]

class TaskResponse(BaseModel):
    task_id: str
    status: str
    paper_id: Optional[str] = None


class TextInput(BaseModel):
    text: str
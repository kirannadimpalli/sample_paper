from pydantic import BaseModel
from typing import List, Optional

class Question(BaseModel):
    question: Optional[str] = None 
    answer: Optional[str] = None
    type: Optional[str] = None
    question_slug: Optional[str] = None
    reference_id: Optional[str] = None
    hint: Optional[str] = None
    params: dict = {}

class Section(BaseModel):
    marks_per_question: Optional[int] = None
    type: Optional[str] = None
    questions: List[Question] = []

class SamplePaper(BaseModel):
    title: Optional[str] = None
    type: Optional[str] = None
    time: Optional[int] = None
    marks: Optional[int] = None 
    params: dict = {}
    tags: List[str] = []
    chapters: List[str] = []
    sections: List[Section] = []

class TaskResponse(BaseModel):
    task_id: str
    status: str
    paper_id: Optional[str] = None


class TextInput(BaseModel):
    text: str
from pydantic import BaseModel
from typing import List

class Score(BaseModel):
    type: str
    score: float

class GradeBase(BaseModel):
    student_id: int
    scores: List[Score] = []
    class_id: int

class GradeIn(GradeBase):
    pass

class GradeOut(GradeBase):
    id: str
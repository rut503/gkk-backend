from fastapi import APIRouter
from bson import ObjectId
from typing import List

from config.datababse import grade_collection
from models.grade_model import GradeIn, GradeOut
from schemas.grade_schemas import grade_serializer, grades_serializer

grade_router = APIRouter()

# get data
@grade_router.get("/grade", response_model=List[GradeOut])
async def get_grades():
    grades = grades_serializer(grade_collection.find().limit(10))
    return grades

@grade_router.get("/grade/{id}", response_model=GradeOut)
async def get_grade(id: str):
    grade = grade_serializer(grade_collection.find_one({"_id": ObjectId(id)}))
    return grade

# post data
@grade_router.post("/grade", response_model=GradeOut)
async def post_grade(grade: GradeIn):
    inserted = grade_collection.insert_one(grade.dict())
    grade = grade_serializer(grade_collection.find_one({"_id": inserted.inserted_id}))
    return grade

# put data
@grade_router.put("/grade/{id}", response_model=GradeOut)
async def put_grade(id: str, grade: GradeIn):
    grade_collection.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": grade.dict()
    })
    updated_grade = grade_serializer(grade_collection.find_one({"_id": ObjectId(id)}))
    return updated_grade

# delete data
@grade_router.delete("/grade/{id}", response_model=GradeOut)
async def delete_grade(id: str):
    deleted_grade = grade_collection.find_one_and_delete({"_id": ObjectId(id)})
    deleted_grade = grade_serializer(deleted_grade)
    return deleted_grade


# EXPERIMENTS
@grade_router.get("/{id}")
async def experiment(id: str):
    
    return "hi" + str(id)
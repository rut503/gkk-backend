def scores_serializer(score) -> dict:
    return {
        "type": score["type"],
        "score": score["score"],
    }

def grade_serializer(grade) -> dict:
    return {
        "id": str(grade["_id"]),
        "student_id": grade["student_id"],
        "scores": [ scores_serializer(score) for score in grade["scores"] ],
        "class_id": grade["class_id"]
    }

def grades_serializer(grades) -> list:
    return [ grade_serializer(grade) for grade in grades ]

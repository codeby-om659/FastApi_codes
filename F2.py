#STUDENT MANAGEMENT API
from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel
app=FastAPI(title="Student Management API")

Student_db={
    101:{"name":"aman","age":20,"course":"B-TECH"},
    102:{"name":"riya","age":21,"course":"BCA"}
}
#Request data Validation ke liye Model
class StudentSchema(BaseModel):
    name:str
    age:int
    course:str

#Update ke liye Model(jahan sare fields optional ho sakte hai)
class StudentUpdateSchema(BaseModel):
    name:str | None=None
    age:int |None=None
    course:str |None =None

#read All(GEt)
@app.get("/student")
def get_all_student():
    return {"student":Student_db}

#create (POST)
@app.post("/student/{student_id}")
def create_student(student_id:int,student:StudentSchema):
    if student_id in Student_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"  {student_id} ID ka student pehle se exist karta hai "
        )
    Student_db[student_id]=student.dict()
    return {"message":"Student Succesfully add ho gaya hai"}

#update/PATCH(resources ka kuch hissa update karen ke kiye)
#put pura object replace karta hai jabki patch se hum sirf wah value change karenge jo userr new bhejega
@app.patch("/student/{student_id}")
def Update_Student_Schema(student_id:int,student:StudentUpdateSchema):
    if student_id not in Student_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f" is {student_id}ka student exist hi nahi karta hai"
        )
    #sirf wahi fields update hogi jo user bhejega
    stored_student=Student_db[student_id]# ye line db mai save student id ki values ko is variable mai store karwa rah ahi
    update_data=student.dict(exclude_unset=True)#user ne jo api ke through new data bheja use ye dictionary mai converrt kar raha hai

    stored_student.update(update_data)#update ek buit in function hai jo purane data main new values ko overwritr karta hai
    return {"message":"student detail update ho gayi","data":stored_student}

#Delete (Resoursec deletekarne ke liye)
@app.delete("/student/{student_id}")
def delete_student(student_id:int):
    if student_id not in Student_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"is {student_id}ID ka student exist nahi karta hai"
        )
    #dict.pop()python dictionary se record remove karta hai
    deleted_student=Student_db.pop(student_id)
    return {"message":f"{student_id}id wala student remove kar diya gay hai"}


from pydantic import BaseModel,EmailStr,Field
from typing import Optional
class Student(BaseModel):

    name: str
    age: int
    standard: str = "12th"  # default value
    medium: Optional[str] = None  # optional field
    email: EmailStr
    cgpa : float=Field( gt=0, lt=10,default=5.0, description="CGPA must be between 0 and 10")  # field with validation


# new_student = {'name': 34, 'age': 19}#throws error as Input should be a valid string
new_student = {'name': 'pooji', 'age': 19, 'email': 'pooji@example.com', 'cgpa': 9}#valid input'}
# new_student1 = {'name': "pooji", 'age': '19', 'email': 'pooji1example.com'}#converts this str to int-->implicit type conversion  #gives email validation error as email is not valid

student= Student(**new_student)
# student1= Student(**new_student1)

print(student)
print(type(student))
# print(student1)

#converting pydantic obj to python dictionary
student_dict = dict(student)
print(student_dict)
#converting pydantic obj to json object
student_json = student.model_dump_json()
print(student_json)
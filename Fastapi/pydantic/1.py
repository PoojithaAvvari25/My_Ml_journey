from pydantic import BaseModel,EmailStr,Field
from typing import List,Dict,Optional,Annotated
#pydantic class
#by default all fields in pydantic model are required
class Schema(BaseModel):
    name: str
    age: Annotated[int,Field(title="name of the patient",description="specift in str format",example=["amit","anand"])]#Annotated-->used to add metadata to the field
    weight: float =Field(gt=0,strict=True,description="Weight of the patient in kg")#gt-->greater than#stict=True makw=e sure that coercing isnot performed
    married: bool=False #default value
    email:EmailStr#pydantic provides built-in validation for email addresses
    allergies:Optional[List[str]]=Field(max_length=30,description="List of allergies of the patient",default=None)
    #specifying DT as list we cant able to validate DT s of vals inside it
    contact_details:Dict[str,str]#using dict we cant able to validate DT s of vals inside it


def create_patient(patient: Schema):
    # Here you can implement the logic to save the patient data to a database or any other storage
    return {"message": "Patient created successfully", "patient": patient}


# # patient1  = Schema(name="John Doe", age='30')#coerces
# patient1  = Schema(name="John Doe", age=30)
# # patient1  = Schema(name="John Doe", age='thirty')#Throws validation error because age is not an integer
# result = create_patient(patient1)
# print(result)  # Output: {'message': 'Patient created successfully', 'patient': {'name': 'John Doe', 'age': 30}}


patient_info = {'name':"abc",'age':30,'weight':70.5,'married':True,'email':'abc@example.com','contact_details':{'email':'abc@example.com','phone':'123-456-7890'}}
patient2 = Schema(**patient_info) #unpacking dictionary to create an instance of Schema
result2 = create_patient(patient2)
print(result2)  # Output: {'message': 'Patient created successfully', 'patient': {'name': 'abc', 'age': 30}}



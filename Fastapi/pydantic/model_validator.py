from pydantic import BaseModel, EmailStr, model_validator ,EmailStr,Field
from typing import Dict, List, Optional


#model_validator is used when we have to work with linked fie;ds..for example here if patient age is greater than 60 he should have emergency contact numberelse we eill return the value error
class Schema(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: Optional[List[str]]=None
    contact_details: Dict[str, str]

    @model_validator(mode='after')  # mode='after' means the validator will be applied after the standard validation
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older than 60 must have an emergency contact')
        return model

def create_patient(patient: Schema):
    # Here you can implement the logic to save the patient data to a database or any other storage
    return {"message": "Patient created successfully", "patient": patient}


patient_info = {'name':"abc",'age':70,'weight':70.5,'married':True,'email':'abc@hdfc.com','contact_details':{'email':'abc@example.com','phone':'123-456-7890','emergency':'987-654-3210'}}
patient2 = Schema(**patient_info) #unpacking dictionary to create an instance of Schema
result2 = create_patient(patient2)
print(result2)
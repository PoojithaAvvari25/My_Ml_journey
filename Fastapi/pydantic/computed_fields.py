#to compute fields based on other fields in the model, we can use the @computed_field decorator. This allows us to define a method that computes a value based on other fields in the model, and then use that computed value as if it were a regular field in the model.
from typing import Dict,List,Optional
from pydantic import BaseModel,computed_field,Field,EmailStr

class Schema(BaseModel):
    name: str
    email: EmailStr
    age: int
    height:float
    weight: float
    married: bool
    allergies: Optional[List[str]]=None
    contact_details: Dict[str, str]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi=self.weight/(self.height**2)
        return round(bmi,2)

def create_patient(patient: Schema):
    # Here you can implement the logic to save the patient data to a database or any other storage
    print(patient.bmi)
    return {"message": "Patient created successfully", "patient": patient}
    



patient_info = {'height':1.75,'name':"abc",'age':70,'weight':70.5,'married':True,'email':'abc@hdfc.com','contact_details':{'email':'abc@example.com','phone':'123-456-7890','emergency':'987-654-3210'}}
patient2 = Schema(**patient_info) #unpacking dictionary to create an instance of Schema
result2 = create_patient(patient2)
print(result2)
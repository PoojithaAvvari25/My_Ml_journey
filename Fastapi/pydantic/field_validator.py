from pydantic import BaseModel,EmailStr,Field,field_validator
from typing import List,Dict,Optional,Annotated
#firld validator--data validation and transformation
class Schema(BaseModel):
    name: str
    age:  int
    weight: float 
    email:EmailStr
    allergies:Optional[List[str]]=Field(max_length=30,description="List of allergies of the patient",default=None)
    contact_details:Dict[str,str]#using dict we cant able to validate DT s of vals inside it


    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        valid_domains=['hdfc.com','icici.com']
        domain_name=value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError(f'Email domain must be one of: {", ".join(valid_domains)}')
        return value

    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()

    @field_validator('age',mode='before')#mode-->specifies when the validator should be applied, either before or after the standard validation like coercion and type checking. The default is 'after', which means the validator will be applied after the standard validation. If you set mode='before', the validator will be applied before the standard validation means coercion.
    @classmethod
    def validate_age(cls, value):
        if value >0 and value < 100:
            raise ValueError('Age must be between 0 and 100')
        return value  #gives error-->python field_validator.py


def create_patient(patient: Schema):
    # Here you can implement the logic to save the patient data to a database or any other storage
    return {"message": "Patient created successfully", "patient": patient}


patient_info = {'name':"abc",'age':'300','weight':70.5,'married':True,'email':'abc@hdfc.com','contact_details':{'email':'abc@example.com','phone':'123-456-7890'}}
patient2 = Schema(**patient_info) #unpacking dictionary to create an instance of Schema
result2 = create_patient(patient2)
print(result2)
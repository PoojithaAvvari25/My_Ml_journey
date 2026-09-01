from pydantic import BaseModel
#to export pydantic objects into diff formats-python dict,json
class Address(BaseModel):
    
    city: str
    state: str
    pin: str

class Patient(BaseModel):

    name: str
    gender: str
    age: int
    height: float=30
    address: Address

address_dict = { 'city' : 'gurgaon', 'state' : 'haryana', 'pin' : '122001' }

address1 = Address(**address_dict)

patient_dict = {'name': 'nitish', 'gender': 'male', 'age': 35, 'address': address1}

patient1 = Patient(**patient_dict)

#converting into python dict
temp=patient1.model_dump()
print(temp)#converting into python dict
temp=patient1.model_dump(include={'name','age'})#include-->specifies which fields to include in the output
print(temp)

temp=patient1.model_dump(exclude_unset=True)#if value isnt specified at time of object creation it isnt included..like optional/default fieldss
print(temp)

#into json
temp2=patient1.model_dump_json(exclude={'address':['state']})#exclude-->specifies which fields to exclude from the output
print(temp2)
from fastapi import FastAPI,Path,HTTPException,Query
# Path--Used to enhance the readability of path parameters
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel ,Field ,computed_field
from typing import Annotated,Literal,Optional
class Patient(BaseModel):
    id: Annotated[str, Field(... , description="The ID of the patient")]
    name: Annotated[str, Field(... , description="The name of the patient")]
    age: Annotated[int, Field(... , description="The age of the patient ",gt=0,lt=150)]
    gender: Annotated[Literal["Male", "Female"], Field(... , description="The gender of the patient")]
    height: Annotated[float, Field(... , description="The height of the patient in mtrs",gt=0)]
    weight: Annotated[float, Field(... , description="The weight of the patient in kgs",gt=0)]
    city: Annotated[str, Field(... , description="The city where the patient lives")]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        bmi = self.bmi
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"


class UpdatedPatient(BaseModel):
    name: Annotated[Optional[str], Field( default=None)]
    age: Annotated[Optional[int], Field(default=None)]
    gender: Annotated[Optional[Literal["Male", "Female"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None,gt=0)]
    weight: Annotated[Optional[float], Field(default=None,gt=0)]
    city: Annotated[Optional[str], Field(default=None)]



app = FastAPI()

def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)

        
@app.get("/")
def hello():
    return {'message': "Patient Management System"}

@app.get("/about")
def about():
    return {'message':'A fully functional API to manage your patient records'}

@app.get("/view")
def view():
    data=load_data()
    return data

@app.get("/view/{patient_id}")
def view_patient(patient_id: str = Path(...,description="The ID of the patient to retrieve",example="P001")):#...-->denotes that field is required
    #load all patients
    data = load_data()
    if patient_id in data:
            return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get('/sort')
def sort_patients(sort_by:str=Query(...,description="The field to sort patients by height,weight,bmi or name",example="name"),order:str=Query('asc'#default
                                                                                                                                              ,description="The order to sort patients by asc or desc",example="asc")):
    if sort_by not in ['height','weight','bmi','name']:
        raise HTTPException(status_code=400, detail="Invalid sort field. Must be one of: height, weight, bmi, name")

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order. Must be either 'asc' or 'desc'")
    data = load_data()
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=(order == 'desc'))
    return sorted_data

@app.post("/create")
def create_patient(patient:Patient):
    #load existing data
    data = load_data()
    #check if patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    #add new patient to db
    data[patient.id] = patient.model_dump(exclude=['id'])

    #save the new dict intp json file
    save_data(data)

    return JSONResponse(status_code=201, content={"message": "Patient created successfully", "patient": patient.model_dump()})

@app.put("/edit/{patient_id}")
def update_patient(patient_id : str ,patient_update:UpdatedPatient):
    data =load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    existing_patient_info = data[patient_id]
    patient_info = patient_update.model_dump(exclude_unset=True)

    for key,value in patient_info.items():
        existing_patient_info[key] = value

    # data[patient_id] = existing_patient_info #but bmi and verdict will remain same
    existing_patient_info['id'] = patient_id
    #convert existing patient info to pydantic object(Patirnt object)
    #then convert pydantic obj to dictionary and conv to dict and update db
    patient_pydantic = Patient(**existing_patient_info)
    updated_patient_info = patient_pydantic.model_dump(exclude=['id'])
    data[patient_id] = updated_patient_info 
    save_data(data)
    return JSONResponse(status_code=200, content={"message": "Patient updated successfully", "patient": existing_patient_info})

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id : str):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404 , detail="Patient not found")

    del data[patient_id]
    save_data(data)

    return JSONResponse(status_code=200 ,content="Patient deleted successfully")
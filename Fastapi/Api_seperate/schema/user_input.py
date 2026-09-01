#pydantic model to validate incoming data

from pydantic import BaseModel,Field,computed_field,field_validator
from typing import Literal,Annotated
from config.city_tier import tier_1_cities,tier_2_cities

class UserInput(BaseModel):
    age:Annotated[int,Field(...,gt=0,lt=110,description="The age of the user")]
    weight:Annotated[float,Field(...,description="weight of te user")]
    height:Annotated[float,Field(...,gt=0,lt=2.5,description="Height of the user")]
    income_lpa:Annotated[float,Field(...,description="Annual income of the user in LPA")]
    smoker:Annotated[bool,Field(...,description="Will user smoke?")]
    city:Annotated[str,Field(...,description="The city in which user lives")]
    occupation:Annotated[Literal['freelancer', 'retired', 'private_job', 'business_owner', 'student'],Field(...,description="Occupation of the user")]


    @computed_field
    @property
    def bmi(self)->float:
        return self.weight/((self.height)**2)
    

    @computed_field
    @property
    def lifestyle_risk(self)->str:
        if self.smoker and self.bmi> 30 :
            return "high"
        elif self.smoker or self.bmi> 27 :
            return "medium"
        else:
            return "low"


    @computed_field
    @property
    def age_group(self)->str:
        if self.age < 25:
            return "young"
        elif self.age < 45 :
            return "adult"
        elif self.age < 60:
            return "middle-aged"
        return "senior"

    @computed_field
    @property
    def city_tier(self)->int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
             return 3

    @field_validator('city')
    @classmethod
    def normalise(cls,v:str)->str:
        v=v.strip().title()
        return v

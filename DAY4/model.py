from pydantic import BaseModel,Field,EmailStr,AnyUrl,field_validator,model_validator,computed_field
from typing import List,Annotated,Optional,Dict


class Address(BaseModel):
    house_number: Annotated[str, Field(min_length=1, max_length=10, description="House/building number")]
    street: Annotated[str, Field(min_length=5, max_length=100, description="Street address")]
    city: Annotated[str, Field(min_length=2, max_length=50, description="City name")]
    postal_code: Annotated[str, Field(pattern=r"^\d{5,6}$", description="Valid postal code")]
    state: Annotated[str, Field(min_length=2, max_length=50, description="State name")]
    country: Annotated[str, Field(min_length=2, max_length=50, description="Country name")]

class Patient(BaseModel):

    name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Give the name of the patient in less than 50 chars', examples=['Nitish', 'Amit'])]
    email: EmailStr
    linkedin_url: AnyUrl
    age: int = Field(gt=0, lt=120)
    weight: Annotated[float, Field(gt=0, strict=True,description="Weight should be in Kilograms")]
    height: Annotated[float, Field(gt=0, strict=True,description="Height should be in Meters")]
    married: Annotated[bool, Field(default=None, description='Is the patient married or not')]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]
    contact_details: Dict[str, str]
    address: Address # Nested Model

    @field_validator("email")
    @classmethod
    def validate_email(cls,email):
        valid_domains=['icici.com','hdfc.com']
        email_domain=email.split('@')[-1]

        if email_domain not in valid_domains:
            raise ValueError("Not a valid domain")
        return email
        
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    
    @field_validator('age',mode="after")
    @classmethod
    def validate_age(cls,age): #afte the type coersion
        if 0<age<120:
            return age
        else:
            raise ValueError("Age should be in between 0 to 120")
    
    @model_validator(mode="after")
    def validate_emergency_contact(cls,model):
        if model.age>60 and 'emergency' not in model.contact_details:
            raise ValueError("Patient older than 60 must have an emergency contact.")
        else:
            return model
    
    @computed_field
    @property
    def bmi(self)->float:
        return round(self.weight/(self.height**2),2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        bmi = self.bmi
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"
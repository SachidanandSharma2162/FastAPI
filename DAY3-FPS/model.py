from fastapi import HTTPException
from pydantic import BaseModel, Field,computed_field,field_validator
from typing import Literal,Annotated,Optional

class Address(BaseModel):
    house_number: Annotated[str, Field(...,min_length=1, max_length=10, description="House/building number")]
    street: Annotated[str, Field(...,min_length=5, max_length=100, description="Street address")]
    city: Annotated[str, Field(...,min_length=2, max_length=50, description="City name")]
    postal_code: Annotated[str, Field(...,pattern=r"^\d{5,6}$", description="Valid postal code")]
    state: Annotated[str, Field(...,min_length=2, max_length=50, description="State name")]
    country: Annotated[str, Field(...,min_length=2, max_length=50, description="Country name")]


class AddressUpdate(BaseModel):
    house_number: Annotated[Optional[str], Field(min_length=1, max_length=10, description="House/building number",default=None)]
    street: Annotated[Optional[str], Field(min_length=5, max_length=100, description="Street address",default=None)]
    city: Annotated[Optional[str], Field(min_length=2, max_length=50, description="City name",default=None)]
    postal_code: Annotated[Optional[str], Field(pattern=r"^\d{5,6}$", description="Valid postal code",default=None)]
    state: Annotated[Optional[str], Field(min_length=2, max_length=50, description="State name",default=None)]
    country: Annotated[Optional[str], Field(min_length=2, max_length=50, description="Country name",default=None)]

class Patient(BaseModel):
    id: str = Field(
        ...,
        min_length=3,
        max_length=10,
        description="Unique patient ID",
        examples=['P001']
    )

    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Patient full name"
    )

    city: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Patient city"
    )

    age: int = Field(
        ...,
        ge=0,
        le=120,
        description="Patient age in years"
    )

    gender: Literal["male", "female", "other"] = Field(
        ...,
        description="Patient gender"
    )

    height: float = Field(
        ...,
        gt=0.5,
        lt=2.5,
        description="Height in meters"
    )

    weight: float = Field(
        ...,
        gt=2,
        lt=300,
        description="Weight in kilograms"
    )

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
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    address: Address

    @field_validator('age',mode="after")
    @classmethod
    def validate_age(cls,age): #afte the type coersion
        if 0<age<120:
            return age
        else:
            raise ValueError("Age should be between 0 and 120")
        
class PatientUpdate(BaseModel):

    name: Annotated[Optional[str],Field(default=None)]
    city: Annotated[Optional[str],Field(default=None)]
    age: Annotated[Optional[int],Field(gt=0,lt=120,default=None)]
    gender: Annotated[Optional[Literal["male","female","other"]],Field(default=None)]
    height: Annotated[Optional[int],Field(default=None,gt=0)]
    weight: Annotated[Optional[int],Field(default=None,gt=0)]
    address: Annotated[Optional[AddressUpdate],Field(default=None)]
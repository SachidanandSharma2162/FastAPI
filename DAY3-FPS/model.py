from pydantic import BaseModel, Field,computed_field
from typing import Literal


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
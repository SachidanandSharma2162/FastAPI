from fastapi import FastAPI, Path,HTTPException
import json


app=FastAPI()

def load_data():
    with open("patients.json","r") as file:
        data=json.load(file)

    return data


@app.get("/")
def home():
    return {"message":"This is home page"}

@app.get("/patients")
def get_patients():
    data = load_data()

    return data

@app.get("/patients/{p_id}")
def get_patient_by_id(p_id:str=Path(...,description="ID of the Patient in the DB",example="P001")):
    patients_data=load_data()

    if p_id in patients_data:
        return patients_data[p_id]
    raise HTTPException(status_code=404,detail="Patient not found!")
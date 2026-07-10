from fastapi import FastAPI, Path,HTTPException,Query
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
def get_patient_by_id(p_id:str=Path(...,description="ID of the Patient in the DB.",example="P001")):
    patients_data=load_data()

    if p_id in patients_data:
        return patients_data[p_id]
    raise HTTPException(status_code=404,detail="Patient not found!")

@app.get("/sort")
def sort_patient(sort_by:str=Query(...,description="sort on the basis of height, weight, bmi and name."),order_by:str=Query('asc',description="Sort in ascending or descending order.")):

    valid_fields=['height','weight','bmi','name','age']
    order_fields=['asc','desc']
    if sort_by not in valid_fields:
        return HTTPException(status_code=400, detail=f'Invalid field, select from {valid_fields}')
    if order_by not in order_fields:
        return HTTPException(status_code=400, detail=f'Invalid order, select from {order_fields}')
    data=load_data()
    patients = list(data.values())

    reverse = True if order_by.lower() == "desc" else False

    # Sort based on given field
    sorted_patients = sorted(
        patients,
        key=lambda x: x.get(sort_by, 0),
        reverse=reverse
    )

    return sorted_patients

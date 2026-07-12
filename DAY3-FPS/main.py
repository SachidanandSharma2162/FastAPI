from fastapi import FastAPI, Path,HTTPException,Query
import json
from model import Patient,PatientUpdate
from database import load_data,save_data
app=FastAPI()
from fastapi.responses import JSONResponse



@app.get("/")
def home():
    return {"message":"This is home page."}

@app.get("/about")
def about():
    return {"message":"This is Patient Monitoring FastAPI System."}
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
        raise HTTPException(status_code=400, detail=f'Invalid field, select from {valid_fields}')
    if order_by not in order_fields:
        raise HTTPException(status_code=400, detail=f'Invalid order, select from {order_fields}')
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


@app.post("/create")
def create_patient(patient:Patient):
    data=load_data()
    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient already exist!")
    
    data[patient.id]=patient.model_dump(exclude=['id'])

    save_data(data=data)
    
    return JSONResponse(status_code=201,content={"message":"Patient created successfully!"})

@app.put("/update/{p_id}")
def update_patient(p_id:str=Path(...,description="ID of the Patient in the DB.",example="P001"), patient:PatientUpdate=None):
    data=load_data()

    if p_id not in data:
        raise HTTPException(status_code=404,detail=f"Patient with the id {p_id} is not present!")
    
    existing_patient=data[p_id]

    update_data=patient.model_dump(exclude_unset=True)

    for key,value in update_data.items():

        if key == "address":
    
            existing_patient["address"].update(
                value
            )
    
        else:
    
            existing_patient[key] = value

    existing_patient['id']=p_id
    patient_pydantic_object=Patient(**existing_patient)
    existing_patient=patient_pydantic_object.model_dump(exclude=['id'])
    data[p_id]=existing_patient
    save_data(data=data)
    
    return JSONResponse(status_code=201,content={"message":"Patient updated successfully!"})
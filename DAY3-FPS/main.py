from fastapi import FastAPI
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
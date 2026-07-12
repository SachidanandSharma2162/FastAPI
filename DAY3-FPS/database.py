import json

def load_data():
    with open("patients.json","r") as file:
        data=json.load(file)

    return data

def save_data(data):

    with open("patients.json","w") as file:
        json.dump(
            data,
            file,
            indent=4
        )

def get_patient(patient_id):

    data = load_data()

    return data.get(patient_id)
from model import Patient

patient={
    "name":"Amit",
    "email":"amit@icici.com",
    "linkedin_url": "http://amit@linkedin.com",
    "age":70,
    "weight":88,
    "height":1.7,
    "married":False,
    "allergies":["Dust"],
    "contact_details":{
        "email":"amit@gmail.com",
        "phone":"9432667214",
        "emergency":"9876234501"
    },
    "address": {
        "house_number": "468/813",
        "street": "Laxmi Nagar",
        "city": "Delhi",
        "postal_code": "110001",
        "state": "Delhi",
        "country": "India"
    }
}

patient1=Patient(**patient) # dictionary unpacking

print(patient1)

patient_dict=patient1.model_dump(exclude_unset=True) # pydantic to python dict
print(patient_dict)
print(type(patient_dict))

patient_json=patient1.model_dump_json()
print(patient_json)
print(type(patient_json))
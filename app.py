# from dotenv import load_dotenv

# load_dotenv()

from flask import Flask, render_template
import json


with open("PatientData.json") as f:
    data = json.load(f)

def set_medication_status(data):
    for patient in data:
        if 'given' not in patient:
            patient['status'] = 'unknown'
        elif patient['given'] == 0:
            patient['status'] = 'red' 
        elif patient['prescribed'] == patient['given']:
            patient['status'] = 'green'
        else:
            patient['status'] = 'orange'
        
    return data


data = set_medication_status(data)

app = Flask(__name__)

@app.route('/')
def hospital():
    wards = list(set([patient["Ward"] for patient in data]))
    return render_template(
        "wards.html",
        data = wards,
    )

@app.route('/<string:ward>')
def wards(ward):
    filtered_data = [patient for patient in data if patient["Ward"] == ward]
    return render_template(
        "patients.html",
        data = filtered_data,
    )



from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import joblib
from keras.models import load_model
import pandas as pd
import numpy as np

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Normalize the data
def normalize_data(scaler, test_df):
    test_df_normal = pd.DataFrame(scaler.transform(test_df), columns=test_df.columns)
    return test_df_normal

# Load the model
def load_models(model_path):
    model = load_model(model_path)
    return model

# Load the scaler
def load_scaler(scaler_path):
    scaler = joblib.load(scaler_path)
    return scaler

# Create dataframe for compute
def create_df(air_temp, process_temp, rotational_speed, torque, tool_wear):
    df = pd.DataFrame({
        'Air temperature [K]': [air_temp],
        'Process temperature [K]': [process_temp],
        'Rotational speed [rpm]': [rotational_speed],
        'Torque [Nm]': [torque],
        'Tool wear [min]': [tool_wear]
    })
    return df

model_path1 = './models/pred_01.h5'
model01 = load_models(model_path1)

scaler_path1 = './models/scaler_pred.pkl'
scaler01 = load_scaler(scaler_path1)

model_path2 = './models/carb_01.h5'
model02 = load_models(model_path2)

scaler_path2 = './models/scaler_carb.pkl'
scaler02 = load_scaler(scaler_path2)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "dynamic_content": "Predictive Maintenance System for Manufacturing"})

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request):
    if request.method == 'POST':
        form_data = await request.form()
        air_temp = float(form_data['air_temp'])
        process_temp = float(form_data['process_temp'])
        rotational_speed = float(form_data['rotational_speed'])
        torque = float(form_data['torque'])
        tool_wear = float(form_data['tool_wear'])
        energy_source = form_data['energy_source']

        # Predictive maintenance
        test_df = create_df(air_temp, process_temp, rotational_speed, torque, tool_wear)
        test_df_normal = normalize_data(scaler01, test_df)
        prediction, prediction_type, _ = predict_failure(model01, test_df_normal)

        # Carbon footprint
        test_df2 = make_df_carb(scaler02, air_temp, process_temp, rotational_speed, torque, tool_wear, energy_source)
        carbon_intensity, carbon_footprint = predict_carbon_footprint(model02, test_df2)

        # Format the output
        confidence_level = round(float(prediction.max()) * 100, 2)
        carbon_intensity = round(float(carbon_intensity), 2)
        carbon_footprint = round(float(carbon_footprint), 2)

        return templates.TemplateResponse("results.html", {
            "request": request,
            "prediction_type": prediction_type,
            "confidence_level": confidence_level,
            "carbon_intensity": carbon_intensity,
            "carbon_footprint": carbon_footprint})

    return templates.TemplateResponse("index.html", {"request": request, "dynamic_content": "Predictive Maintenance System for Manufacturing"})

# Make dataframe for carbon footprint calculations
def make_df_carb(scaler, air_temp, process_temp, rotational_speed, torque, tool_wear, energy_source):
    power_consumption = torque * rotational_speed * 0.1047 / 0.8
    time_hr = tool_wear / 60
    energy_consumption = power_consumption * time_hr / 1000

    energy_diesel = 0
    energy_grid	= 0
    energy_gas = 0
    
    if energy_source == '1':
        energy_gas = 1
    elif energy_source == '2':
        energy_diesel = 1
    elif energy_source == '3':
        energy_grid = 1
    else:
        energy_diesel = 0
        energy_grid	= 0
        energy_gas = 0

    test_df_num = pd.DataFrame({'Air temperature [K]': [air_temp], 'Process temperature [K]': [process_temp], 
                            'Rotational speed [rpm]': [rotational_speed], 'Torque [Nm]': [torque], 
                            'Tool wear [min]': [tool_wear], 'Power Consumption (W)': [power_consumption],
                            'Time (Hours)': [time_hr],
                            'Energy Consumption (kWh)': [energy_consumption]})
    test_df_cat = pd.DataFrame({'Energy Source_Diesel': [energy_diesel],
                        'Energy Source_Grid Electricity': [energy_grid], 
                        'Energy Source_Natural Gas': [energy_gas]})

    test_df_norm = normalize_data(scaler, test_df_num)
    test_df = pd.concat([pd.DataFrame(test_df_norm, columns=test_df_num.columns), test_df_cat], axis=1)
    return test_df

# Predict the failure
def predict_failure(model, test_data):
    prediction = model.predict(test_data)
    max_prediction_index = np.argmax(prediction)

    failure_types = ['Heat Dissipation Failure', 'No Failure', 'Overstrain Failure', 'Power Failure', 'Tool Failure']
    prediction_type = failure_types[max_prediction_index]
    
    return prediction, prediction_type, max_prediction_index

# Calculate carbon intensity and footprint
def predict_carbon_footprint(model, test_df):
    prediction = model.predict(test_df)
    carbon_intensity = prediction[0][0]
    carbon_footprint = prediction[0][1]
    
    return carbon_intensity, carbon_footprint

    
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import joblib

from flask import Flask, request, jsonify
from flask import render_template

app = Flask(__name__)

# Normalize the test data
def normalize_test_data(scaler, test_df):
    test_df_norm = pd.DataFrame(scaler.transform(test_df), columns=test_df.columns)
    return test_df_norm

# Load the model
def load_trained_model(model_path):
    model = load_model(model_path)
    return model

# Load the scaler
def load_scaler(scaler_path):
    scaler = joblib.load(scaler_path)
    return scaler

# Make dataframe for predictive maintenance
def make_df_pred(air_temp, process_temp, rotational_speed, torque, tool_wear):
    test_df = pd.DataFrame({'Air temperature [K]': [air_temp], 
                            'Process temperature [K]': [process_temp], 
                            'Rotational speed [rpm]': [rotational_speed], 
                            'Torque [Nm]': [torque], 
                            'Tool wear [min]': [tool_wear]})
    return test_df

# Make dataframe for carbon footprint calculations
def make_df_carb(scaler, air_temp, process_temp, rotational_speed, torque, tool_wear, energy_source):
    power_consumption = torque * rotational_speed * 0.1047 / 0.8
    time_hr = tool_wear / 60
    energy_consumption = power_consumption * time_hr / 1000

    energy_diesel = 0
    energy_grid	= 0
    energy_gas = 0

    if energy_source == 'Natural Gas':
        energy_gas = 1
    elif energy_source == 'Diesel':
        energy_diesel = 1
    elif energy_source == 'Grid Electricity':
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

    test_df_norm = normalize_test_data(scaler, test_df_num)
    test_df = pd.concat([pd.DataFrame(test_df_norm, columns=test_df_num.columns), test_df_cat], axis=1)
    return test_df

# Predict the failure
def predict_failure(model, test_data):
    prediction = model.predict(test_data)
    max_prediction_index = np.argmax(prediction)

    failure_types = ['Heat Dissipation Failure', 'No Failure', 'Overstrain Failure', 'Power Failure', 'Tool Failure']
    prediction_type = failure_types[max_prediction_index]
    
    return prediction, prediction_type, max_prediction_index

# Calculate carbon intensity and foot print
def predict_carbon_footprint(model, test_df):
    prediction = model.predict(test_df)
    carbon_intensity = prediction[0][0]
    carbon_footprint = prediction[0][1]
    return carbon_intensity, carbon_footprint


@app.route('/predict', methods=['GET','POST'])
def predict():
    # Load model and scaler
    model_path_01 = r'.\models\pred_01.h5'
    model_01 = load_trained_model(model_path_01)

    scaler_path_01 = r'.\models\scaler_pred.pkl'
    scaler_01 = load_scaler(scaler_path_01)

    model_path_02 = r'.\models\carb_01.h5'
    model_02 = load_trained_model(model_path_02)

    scaler_path_02 = r'.\models\scaler_carb.pkl'
    scaler_02 = load_scaler(scaler_path_02)

    if request.method == 'POST':
        air_temp = float(request.form['air_temp'])
        process_temp = float(request.form['process_temp'])
        rotational_speed = float(request.form['rotational_speed'])
        torque = float(request.form['torque'])
        tool_wear = float(request.form['tool_wear'])
        energy_source = request.form['energy_source']

        # Inference for predictive maintenance
        test_df_01 = make_df_pred(air_temp, process_temp, rotational_speed, torque, tool_wear)
        test_df_norm_01 = normalize_test_data(scaler_01, test_df_01)
        prediction, prediction_type, _ = predict_failure(model_01, test_df_norm_01)

        # Inference for carbon footprint calculations
        test_df_02 = make_df_carb(scaler_02, air_temp, process_temp, rotational_speed, torque, tool_wear, energy_source)
        carbon_intensity, carbon_footprint = predict_carbon_footprint(model_02, test_df_02)
        
        # Format the output
        confidence_level = round(float(prediction.max() * 100), 2)
        carbon_intensity = round(float(carbon_intensity), 2)
        carbon_footprint = round(float(carbon_footprint), 2)
        return render_template('result.html', prediction_type=prediction_type, 
                               confidence_level=confidence_level, 
                               carbon_intensity=carbon_intensity, 
                               carbon_footprint=carbon_footprint)
    return render_template('index.html')

    """
    # Prepare response
    response = {
        'prediction_type': prediction_type,
        'confidence_level': float(prediction.max() * 100)
    }

    return jsonify(response)
    """




if __name__ == '__main__':
    app.run()
    print("loading model01")
    # Load model and scaler
    model_path_01 = r'.\models\pred_01.h5'
    model_01 = load_trained_model(model_path_01)
    print("Done loading model01" )


    print("loading scaler_01")

    scaler_path_01 = r'.\models\scaler_pred.pkl'
    scaler_01 = load_scaler(scaler_path_01)
    print("Done loading scaler_01" )

    print("loading model02")

    model_path_02 = r'.\models\carb_01.h5'
    model_02 = load_trained_model(model_path_02)
    # Load model and scaler
    print("Done loading model02" )

    print("loading scaler_02")

    scaler_path_02 = r'.\models\scaler_carb.pkl'
    scaler_02 = load_scaler(scaler_path_02)
    print("loading scaler_02")

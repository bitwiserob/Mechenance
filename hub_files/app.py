import pandas as pd
import numpy as np
import joblib
from keras.models import load_model
from flask import Flask, request, jsonify
from flask import render_template
import json
import plotly
import plotly.graph_objs as go

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



@app.route('/')
def index():
    return render_template('index.html')

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
    
    failure_types = ['Heat Dissipation Failure', 'No Failure', 'Overstrain Failure', 'Power Failure', 'Tool Failure']
    predictions = prediction[0]
    print(predictions)
    data = [go.Bar(x= failure_types, y=predictions, marker=dict(color='rgb(158,202,225)'))]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('result.html', prediction_type=prediction_type, 
                            confidence_level=confidence_level, 
                            carbon_intensity=carbon_intensity, 
                            carbon_footprint=carbon_footprint,
                            graphJSON=graphJSON)


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

from flask import Flask
from flask import render_template,request
from flask_bootstrap import Bootstrap
import plotly.graph_objs as go
import plotly
import json

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')




@app.route('/predict', methods=['GET', 'POST'])
def predict():
    form_data = {}
    if request.method == 'POST':
        # Assuming you're sending data with the keys 'air_temp', 'rpm', 'nm', 'min'
        form_data['air_temp'] = request.form.get('air_temp', '')
        form_data['rpm'] = request.form.get('rpm', '')
        form_data['nm'] = request.form.get('nm', '')
        form_data['min'] = request.form.get('min', '')
    data = [go.Bar(x=[1, 2, 3], y=[4, 5, 6])]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('predict.html', form_data=form_data,graphJSON=graphJSON)

    
if __name__ == '__main__':
    app.run(debug=True)
#load model on startup
from flask import Flask
from flask import render_template,request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    form_data = {}
    if request.method == 'POST':
        # Assuming you're sending data with the keys 'air_temp', 'rpm', 'nm', 'min'
        form_data['air_temp'] = request.form.get('air_temp_input', '')
        form_data['rpm'] = request.form.get('rpm_input', '')
        form_data['nm'] = request.form.get('nm_input', '')
        form_data['min'] = request.form.get('min_input', '')
    return render_template('predict.html', form_data=form_data)

if __name__ == '__main__':
    app.run(debug=True)
#load model on startup
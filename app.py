from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import pickle
import os

app = Flask(__name__)
model_path = os.path.join(os.getcwd(), 'model.pkl')

with open(model_path, 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form

    # Mapping 
    gender = 0 if data['Gender'] == 'Male' else 1
    customer_type = 1 if data['Customer Type'] == 'Loyal Customer' else 0
    travel_type = 0 if data['Type of Travel'] == 'Business travel' else 1
    flight_class = {'Eco': 0, 'Eco Plus': 1, 'Business': 2}[data['Class']]

    input_df = pd.DataFrame([{
        'Gender': gender,
        'Customer Type': customer_type,
        'Age': int(data['Age']),
        'Type of Travel': travel_type,
        'Class': flight_class,
        'Flight Distance': int(data['Flight Distance']),
        'Seat comfort': int(data['Seat comfort']),
        'Departure/Arrival time convenient': int(data['Departure/Arrival time convenient']),
        'Food and drink': int(data['Food and drink']),
        'Gate location': int(data['Gate location']),
        'Inflight wifi service': int(data['Inflight wifi service']),
        'Inflight entertainment': int(data['Inflight entertainment']),
        'Online support': int(data['Online support']),
        'Ease of Online booking': int(data['Ease of Online booking']),
        'On-board service': int(data['On-board service']),
        'Leg room service': int(data['Leg room service']),
        'Baggage handling': int(data['Baggage handling']),
        'Checkin service': int(data['Checkin service']),
        'Cleanliness': int(data['Cleanliness']),
        'Online boarding': int(data['Online boarding']),
        'Departure Delay in Minutes': int(data['Departure Delay in Minutes']),
        'Arrival Delay in Minutes': int(data['Arrival Delay in Minutes']),
    }])

    prediction = model.predict(input_df)[0]
    result = "Satisfied" if prediction == 1 else "Not Satisfied"

    return render_template('predict.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)

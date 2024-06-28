import numpy as np
import pickle
import pandas as pd
import os
from flask import Flask, request, render_template

app = Flask(__name__)
model = pickle.load(open(r'radf.pkl', 'rb'))
tsg = pickle.load(open(r'tsg.pkl','rb'))
@app.route('/')  # rendering the HTML template
def home():
    return render_template('index.html')

@app.route('/submit', methods=["POST", "GET"])
def submit():
    # Read the inputs given by the user
    Pclass = int(request.form['Pclass'])
    Sex = request.form['Sex']  # Add Sex as an input
    Age = int(request.form['Age'])
    SibSp = int(request.form['SibSp'])
    Parch = int(request.form['Parch'])
    Fare = int(request.form['Fare'])

    # Create a dictionary with the input data
    input_data = {
        'Pclass': Pclass,
        'Sex': Sex,
        'Age': Age,
        'SibSp': SibSp,
        'Parch': Parch,
        'Fare': Fare
    }

    # Predict using the loaded model file
    # You should preprocess the 'Sex' feature before passing it to the model
    # For example, you can use one-hot encoding
    input_data['Sex'] = 1 if input_data['Sex'] == 'male' else 0

    # Ensure that the features are in the correct order and format
    input_features = [input_data['Pclass'], input_data['Sex'], input_data['Age'], input_data['SibSp'],
                      input_data['Parch'], input_data['Fare']]

    prediction = model.predict([input_features])
    print(prediction)
    prediction = int(prediction)
    print(type(prediction))

    if prediction == 0:
        return render_template("index.html", result="did not survive")
    else:
        return render_template("index.html", result="survived")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False)
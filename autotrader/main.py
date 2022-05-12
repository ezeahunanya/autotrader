import os
import sys
PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path = [PROJ_DIR] + sys.path
from utils import  load_pickle, MODEL_FEATURES
import pandas as pd
import numpy as np

from flask import Flask, request, render_template

app = Flask(__name__)

def predict_controller(request: request) -> float:
    feature_values = {feature: request.form.get(feature, type=float) for feature in MODEL_FEATURES}
    feature_values = pd.DataFrame(data=feature_values, index=[0])[MODEL_FEATURES].values 

    model = load_pickle(PROJ_DIR+'/models/price_prediction_model.pkl')
    inverse_transform = lambda x: np.exp(x)-1 # HAAACKY  this is cause we transform the target variable for the model, but this inverse transform should be done in model training. Fix later 
    prediction = model.predict(feature_values)
    prediction = round(float(inverse_transform(prediction)), 3)

    return prediction

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template('predict.html')
    elif request.method == 'POST':
        return {'price_prediction': predict_controller(request)}



if __name__ == '__main__':
    app.run(debug=True)
import os
import sys
PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path = [PROJ_DIR] + sys.path
from utils import  load_pickle, MODEL_FEATURES
import pandas as pd

from flask import Flask, request, render_template

app = Flask(__name__)

def predict_controller(request: request) -> float:
    feature_values = {feature: request.form.get(feature, type=float) for feature in MODEL_FEATURES}
    feature_values = pd.DataFrame(data=feature_values, index=[0])[MODEL_FEATURES].values 

    model = load_pickle(PROJ_DIR+'/models/price_prediction_model.pkl')
    prediction = round(float(model.predict(feature_values)), 3)

    return prediction

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template('predict.html')
    elif request.method == 'POST':
        return {'price_prediction': predict_controller(request)}



if __name__ == '__main__':
    app.run(debug=True)
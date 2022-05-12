import os
import sys
PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path = [PROJ_DIR] + sys.path
from utils import  load_pickle, MODEL_FEATURES
import pandas as pd
import numpy as np
from typing import Dict

from flask import request

def predict_controller(request: request) -> Dict:

    feature_values = {feature: request.form.get(feature, type=float) for feature in MODEL_FEATURES}
    feature_values = pd.DataFrame(data=feature_values, index=[0])[MODEL_FEATURES].values.reshape(1, len(MODEL_FEATURES))

    model = load_pickle(PROJ_DIR+'/models/price_prediction_model.pkl')
    shap_explainer = load_pickle(PROJ_DIR+'/models/price_prediction_shap_explainer.pkl')
    inverse_transform = lambda x: np.exp(x)-1 # HAAACKY  this is cause we transform the target variable for the model, but this inverse transform should be done in model training. Fix later 
    prediction = model.predict(feature_values)
    prediction = round(float(inverse_transform(model.predict(feature_values))), 3)
    prediction_payload = {
        'price': prediction,
        'shap_values': {feature:shap_value for feature, shap_value in zip(MODEL_FEATURES, shap_explainer(feature_values).values.tolist()[0])}
    }

    return prediction_payload
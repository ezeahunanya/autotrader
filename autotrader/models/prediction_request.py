import os
import sys
PROJ_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path = [PROJ_DIR] + sys.path
from functools import cached_property
from utils import  sort_dict_by_value, load_pickle, MODEL_FEATURES
import pandas as pd
import numpy as np
from typing import Dict, Union
from flask import request


class PredictionRequest:
    PREDICTION_MODEL = load_pickle(PROJ_DIR+'/models/price_prediction_model.pkl')
    SHAP_EXPLAINER = load_pickle(PROJ_DIR+'/models/price_prediction_shap_explainer.pkl')
    MODEL_FEATURES = MODEL_FEATURES

    def __init__(self, request: request):
        self.request = request
        self.data = request.get_json()
        self.ip_address = request.remote_addr

    @cached_property # this decorator means that when a new PredictionRequest object is instantiated this method is calculated and stored in an attribute of the same name. The 'cached' bit means this attribute is calculated once and stored in the cache (i.e. memory). So when this attribute is called again, it isn't re-calculated but just called from memory.
    def feature_values(self) -> np.ndarray:
        feature_values = pd.DataFrame(data=self.feature_values_for_db, index=[0])[self.MODEL_FEATURES].values.reshape(1, len(self.MODEL_FEATURES))            
        return feature_values

    @cached_property
    def feature_values_for_db(self) -> Dict[str, float]:
        feature_values_for_db = {feature: float(self.data[feature]) for feature in self.MODEL_FEATURES}
        return feature_values_for_db

    @cached_property
    def prediction(self) -> float:
        price_transform = lambda x: np.exp(x)-1 # Necessary because model predicts the log of price. Perhaps this logic should be moved into the model.
        unformatted_prediction = self.PREDICTION_MODEL.predict(self.feature_values)
        formatted_prediction = round(float(price_transform(unformatted_prediction)), 3)
        return formatted_prediction 
    
    @cached_property
    def shap_values(self) -> Dict[str, float]:
        unformatted_shap_values = self.SHAP_EXPLAINER(self.feature_values)
        formatted_shap_values = [round(sv,4) for sv in unformatted_shap_values.values[0].tolist()]
        shap_dictionary = {feature:sv for feature, sv in zip(self.MODEL_FEATURES, formatted_shap_values)}
        return sort_dict_by_value(shap_dictionary)

    @cached_property
    def response(self) -> Dict[str, Union[float, dict]]:
        return { 'price_prediction': self.prediction, 'shap_values': self.shap_values} 

    def __repr__(self) -> str:
        return f'PredictionRequest(ip_address={self.ip_address})'


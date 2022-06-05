import os
import sys
import logging 

PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path = [PROJ_DIR] + sys.path

from flask import Flask, request, render_template
from flask_cors import CORS
from models.prediction_request import PredictionRequest
from sqlalchemy.orm import Session
from db.database import engine
from db.schema import Prediction

# Setting up root logger
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)

file_handler = logging.FileHandler(PROJ_DIR+'/autotrader/logs/app.log')
file_handler.setLevel(logging.INFO)

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(module)s %(name)s %(message)s',
    handlers=[file_handler, stream_handler]
    )


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)

@app.route("/", methods=['GET', 'POST'])
def predict(write_to_db: bool = True):
    if request.method == 'GET':
        return render_template('predict.html')
    else:
        prediction_request = PredictionRequest(request=request)
        if write_to_db:
            store_prediction(prediction_request)
        return prediction_request.response

def store_prediction(prediction_request: PredictionRequest) -> None:
    with Session(engine) as session:
        prediction_record = Prediction(
            price_prediction = prediction_request.prediction,
            feature_values = prediction_request.feature_values_for_db,
            shap_values = prediction_request.shap_values,
            ip_address = prediction_request.ip_address
            )
        session.add(prediction_record)
        session.commit()
        

if __name__ == '__main__':
    app.run()
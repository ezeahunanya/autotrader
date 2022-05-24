import os
import sys
from flask import Flask
PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path = [PROJ_DIR] + sys.path


from flask import Flask, request, render_template
from models.prediction_request import PredictionRequest
from sqlalchemy.orm import Session
from db.database import engine
from db.models import Prediction


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False # This ensures that the jsons returned to the client preserve their order that exists when we send off our python dictionary. The default is for flask to order it by key.

@app.route("/predict", methods=['GET', 'POST'])
def predict(write_to_db: bool = True):
    if request.method == 'GET':
        return render_template('predict.html')
    else:
        prediction_request = PredictionRequest(request=request)
        if write_to_db:
            store_prediction(prediction_request)
        return prediction_request.response

def store_prediction(prediction_request: PredictionRequest) -> None:

    with Session(engine) as session: # should probably put this in a try/except block
        prediction_record = Prediction(
            price_prediction = prediction_request.prediction,
            feature_values = prediction_request.feature_values_for_db,
            shap_values = prediction_request.shap_values,
            ip_address = prediction_request.ip_address
            )
        session.add(prediction_record)
        session.commit()


if __name__ == '__main__':
    app.run(debug=True)
import os
import sys
PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path = [PROJ_DIR] + sys.path

from controller import predict_controller
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template('predict.html')
    elif request.method == 'POST':
        return {'prediction_details': predict_controller(request)}



if __name__ == '__main__':
    app.run(debug=True)
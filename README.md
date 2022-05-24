# Autotrader

A machine learning server and scraper which allows users to input vehicle features into a (soon to be) pretty UI and get back a price prediction and shapley values to help the user understand the relationship between their feature values and the model's prediction. The prediction model is an XGBoost regression model trained on over 8000 vehicle records, the training script for this model is included in this repo and evaluation metrics can be found in `models/price_prediction_metrics.json`. The training data for the model was scraped from the autotrader website.


## Running locally

### Running Natively

Things you will need installed:

1. PostgreSQL (if you're on macOS you can use home brew to install and run the postgres server, if you're on windows 🤷🏿‍♂️ ... gonna have to google mate soz)
2. Python 3.8 (and ideally a virtual environment manager e.g. pyenv or virtualenv)
   

Setup:

1. Install python dependencies using `pip install -r requirements.txt`.
2. Create the `autotrader` user and `autotrader_development` database on your local postgres instance. This 
can be done whilst inside the psql console with:

        CREATE USER autotrader;
        CREATE DATABASE autotrader_development;

3. Run `python autotrader/main.py` to start the flask server and go to `localhost:5000/predict` in your brower to use the app.

### Running from Docker

...coming soon. 

## Prediction Model

There are 2 stages in the price prediction model pipeline:

1. `scripts/preprocess_price_prediction_model.py` cleans the scraped data and and outputs model ready training data to `data/training_data.csv`.
2. `scripts/train_price_prediction_model.py` trains the model using training data from :point_up: and creates `models/price_prediction_model.pkl` and `models/price_prediction_metrics.json`.
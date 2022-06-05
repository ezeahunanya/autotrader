# Autotrader

A machine learning api and scraper which servers the [autotrader-client](https://github.com/Primebrook/autotrader-client). It
allows users to input their vehicle attributes and get back a car price prediction along with shapley values to help users understand the relationship between their vehicle attributes values and the price prediction. The prediction model is an XGBoost regression model trained on over 8000 vehicle records, the training script for this model is included in this repo and evaluation metrics can be found in `models/price_prediction_metrics.json`. The training data for the model was scraped from the autotrader website.


## Running locally

### Running Natively

Things you will need installed:

1. PostgreSQL (if you're on macOS you can use Homebrew to install and run the postgres server)
2. Python 3.8> (and ideally a virtual environment manager e.g. pyenv or virtualenv)
   

Setup:

1. Install python dependencies using `pip install -r requirements.txt`.
2. Create the `autotrader` user and `autotrader_development` database on your local postgres instance. This 
can be done whilst inside the psql console with:

        CREATE USER autotrader;
        CREATE DATABASE autotrader_development;

1. Run `FLASK_ENV=development python autotrader/app.py` to start the flask server in development mode and go to `http://localhost:5000` in your browser to get a prediction.

### Running from Docker

...coming soon. 

## Prediction Model

There are 2 stages in the price prediction model pipeline:

1. `scripts/preprocess_price_prediction_model.py` cleans the scraped data and and outputs model ready training data to `data/training_data.csv`.
2. `scripts/train_price_prediction_model.py` trains the model using training data from :point_up: and creates `models/price_prediction_model.pkl` and `models/price_prediction_metrics.json`.
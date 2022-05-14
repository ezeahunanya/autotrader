# Autotrader

A machine learning flask server, client and scraper which allows users to input vehicle features into a (soon to be) pretty UI and get back a price prediction and shapley values to help the user understand the relationship between their feature values and the model's prediction. The prediction model is an XGBoost regression model trained on over 8000 vehicle records, the training script for this model is included in this repo. The training data for the model was scraped from the autotrader website.


## Running locally

Things you will need installed:

1. PostgreSQL (if you're on macOS you can use home brew to install and run the postgres server, if you're on windows 🤷🏿‍♂️ ... gonna have to google)
2. Python 3.8.x (and ideally a virtual environment manager e.g. pyenv or virtualenv)
   

Setup:

1. Install python dependencies using `pip install -r requirements.txt`.
2. Create the `autotrader` user and `autotrader_development` database on your local postgres instance. This 
can be done whilst inside the psql console with:

        CREATE USER autotrader;
        CREATE DATABASE autotrader_development;

3. Run `python -m autotrader.database` in the root directory of the project to connect to the db and create the tables (at the moment only only one table)
4. Run `python autotrader/main.py` to start the flask server and go to `localhost:5000/predict` in your brower to use the app.



## Scraper

[Autotrader_scraper](/autotrader_scraper) contains a scrapy project to gather 
car infomation from the autotrader website and store it inside a database.

To run the scraper, change the working directory to 'autotrader_scraper' 
from the command line. Then run the following command:

```
scrapy crawl autotrader
```



## Prediction Model

There are 2 stages in the price prediction model pipeline:

1. `scripts/preprocess_price_prediction_model.py` cleans the scraped data and and outputs model ready training data to `data/training_data.csv`.
2. `scripts/train_price_prediction_model.py` trains the model useing training data from :point_up: and creates `models/price_prediction_model.pkl` and `models/price_prediction_metrics.json`.
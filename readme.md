# Autotrader

Autotrader analyses car features from the autotrader website. This project
is split into to three sections:

- Gathering data into a database
- EDA
- Modeling

[Autotrader_scraper](/autotrader_scraper) contains a scrapy project to gather 
car infomation from the autotrader website and store it inside a database.

## Installation

To run this project install [python](https://www.python.org/downloads/). 
Clone the GitHub repository by running the following in the command line:
```
git clone https://github.com/ezeahunanya/autotrader.git
```

Install the packages in the `requirements.txt` file.

To run the scraper, change the working directory to 'autotrader_scraper' 
from the command line. Then run the following command:

```
scrapy crawl autotrader
```

## Prediction Model

To create the training data for the price prediction model run: 
```
python scripts/preprocess_price_prediction_model.py
```

This will output training data to `data/training_data.csv`. To train the model using this training data run: 
```
python scripts/train_price_prediction_model.py
``` 
This will output the trained model and the model metrics (optimized hyperparameters, evaluation metrics and feature importances) and save to `models/`.


## Flask App

What's this for? We'll have a server and client: 

    - There will be a page on the client which will take post requests of feature inputs to the price prediction model we'll use this to predict the price for a car with these features.
    - We'll return the price prediction plus the shapley values to show which feature was most important for this prediction. We'll store these predictions plus shapley values in a database.

To start flask app in development mode, run `python autotrader/main.py`. This should start the server from port 5000. Got to `localhost:5000/predict` in your browser and input feature values, after hitting sumbit you should get a price prediction back.
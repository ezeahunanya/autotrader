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


To create the training data for the price prediction model run `python scripts/preprocess_price_prediction_model.py`. This will output training data to `data/training_data.csv`.
To train the model run `python scripts/train_price_prediction_model.py`. This will output the trained model and the model metrics (optimized hyperparameters, evaluation metrics, feature importances) and save to `models/`.

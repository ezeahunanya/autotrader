import os
import sys
PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path = [PROJ_DIR] + sys.path

from utils import save_as_pickle, save_as_json, MODEL_FEATURES
from pprint import pprint
from typing import Dict, Tuple, Callable, Union, Any

import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from hyperopt import fmin, tpe, hp, STATUS_OK, space_eval, Trials
from xgboost import XGBRegressor


def mae(y_true: np.ndarray, y_preds: np.ndarray) -> float:
    mae = float(np.mean(np.abs(y_true - y_preds)))
    return mae

def mse(y_true: np.ndarray, y_preds: np.ndarray) -> float:
    mse = float(np.mean(np.square(y_true - y_preds)))
    return mse

def metric_result(metric: str, metrics_array: np.ndarray) ->  Dict[str, float]:
    return {'mean_val': float(metrics_array[metric].mean()), 'stdev': float(metrics_array[metric].std())}

def sort_dict_by_value(dct: Dict[Any, Union[float, int]]) -> Dict[Any, Union[float, int]]:
    return { k: v for k, v in sorted(dct.items(), key = lambda item: item[1], reverse=True) }

def kfold_scorer(X: pd.DataFrame, y: pd.DataFrame, folds: int = 10) -> Callable:
    def objective(params: Dict) -> Dict:
        regressor = XGBRegressor(**params)
        kf = KFold(n_splits=folds, shuffle=True, random_state=42)
        metrics_for_all_folds = np.array([], dtype=[('rmse', 'float32'), ('mae', 'float32'), ('mse', 'float32')])
        for train_indices, test_indices in kf.split(X, y):
            X_train_fold, X_test_fold = X.iloc[train_indices], X.iloc[test_indices]
            y_train_fold, y_test_fold = y.iloc[train_indices], y.iloc[test_indices]
            regressor.fit(X_train_fold.values, y_train_fold.values)
            y_preds = regressor.predict(X_test_fold.values)
            mae_score = mae(y_test_fold.values, y_preds)
            mse_score = mse(y_test_fold.values, y_preds)
            rmse_score = np.sqrt(mse_score)
            metrics_for_all_folds = np.append(
                metrics_for_all_folds,
                np.array([(mae_score, mse_score, rmse_score)], dtype=[("mae", "float32"), ("mse", "float32"), ("rmse", "float32")])
                )

        loss = metric_result('rmse', metrics_for_all_folds)['mean_val']
        results = { 'loss': loss, 'status': STATUS_OK }
        y_interquartile_range = y.describe()['75%'] - y.describe()['25%']
        for metric in metrics_for_all_folds.dtype.names:
            results[metric] = metric_result(metric, metrics_for_all_folds)
            results[metric+'_percentage_of_iqr'] = 100*results[metric]['mean_val']/y_interquartile_range
        return results
    return objective

def optimize_hyperparams(X: pd.DataFrame, y: pd.DataFrame) -> Tuple[dict, Trials]:
    space = {
        'verbosity': 0,
        'learning_rate': hp.choice('learning_rate', np.arange(0.001, 0.99, 0.001)),
        'max_depth': hp.choice('max_depth', np.arange(2, 10, 1, dtype=int)),
        'min_child_weight': hp.choice('min_child_weight', np.arange(1, 10, 1, dtype=int)),
        'colsample_bytree': hp.choice('colsample_bytree', np.arange(0.1, 1.0, 0.1)),
        'subsample': hp.uniform('subsample', 0.5, 1),
        'n_estimators': hp.choice('n_estimators', np.arange(1, 200, 1))
    }
    trials = Trials()
    best = fmin(
        fn=kfold_scorer(X, y),
        space=space,
        algo=tpe.suggest,
        max_evals=100,
        trials=trials
    )
    best_params = space_eval(space, best)
    return best_params, trials
    
def main(X: pd.DataFrame, y: pd.DataFrame) -> Tuple[XGBRegressor, dict]:
    best_params, trials = optimize_hyperparams(X, y)
    model = XGBRegressor(**best_params)
    model.fit(X.values, y.values)

    int64_to_int = lambda x: int(x) if type(x) == np.int64 else x
    best_params = {k:int64_to_int(v) for k, v in best_params.items()} # np.int64 objects are not JSON serializable
    feature_importances = sort_dict_by_value(
        {feature: importance for feature, importance in zip(X.columns.to_list(), model.feature_importances_.tolist())}
    )
    model_details = {
        'best_params': best_params,
        'best_trial': trials.best_trial['result'],
        'feature_importances': feature_importances
    }
    return model, model_details



if __name__ == '__main__':
    training_data = pd.read_csv(PROJ_DIR+'/data/training_data.csv')
    X = training_data[MODEL_FEATURES]
    y = training_data['price'].apply(lambda x: np.log(1+x)) # Changing target variable to log of price cause price is massively right skewed. Should we transform back to price before model predicts?
    model, model_details = main(X, y)
    pprint(model_details, sort_dicts=False)
    print(f"\nThe average root meat squared percentage error (of the interquartile range) for this model is {round(model_details['best_trial']['rmse_percentage_of_iqr'], 2)}%")
    save_as_pickle(obj=model, filepath=PROJ_DIR+'/models/price_prediction_model.pkl')
    save_as_json(obj=model_details, filepath=PROJ_DIR+'/models/price_prediction_metrics.json')
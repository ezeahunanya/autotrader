import pandas as pd
from sklearn.feature_selection import mutual_info_regression

def get_label_encoding_for_categoricals(df):
    '''
    Return a dataframe with label encoding for categorical columns.
    ''' 

    df = df.copy()
    for col in df.select_dtypes("category"):
        df[col], _ = df[col].factorize()

    return df


def make_mi_scores(X, y):
    '''
    Return a data series with mutual infomation of the columns.
    '''
    
    discrete_features = X.dtypes == int
    mi_scores = mutual_info_regression(X, y, discrete_features=discrete_features)
    mi_scores = pd.Series(mi_scores, name="MI Scores", index=X.columns)
    mi_scores = mi_scores.sort_values(ascending=False)
    
    return mi_scores
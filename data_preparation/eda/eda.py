import pandas as pd
from sklearn.feature_selection import mutual_info_regression
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

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

def plot_mi_scores(scores):
    '''
    Plots mutual information scores on bar chart.
    '''

    plt.figure(figsize=(8, 10))
    scores = scores.sort_values(ascending=True)
    width = np.arange(len(scores))
    ticks = list(scores.index)
    plt.barh(width, scores)
    plt.yticks(width, ticks)
    plt.title("Mutual Information Scores")

def plot_price_histogram(df):
    '''
    Plots price histogram.
    '''    
    
    binsize = 1000
    bins = np.arange(0, df.price.max()+binsize, binsize)

    plt.figure(figsize=[8, 5])
    plt.hist(data = df, x = 'price', bins = bins)
    plt.xlabel('Price (£)')
    plt.ylabel('Frequency')
    plt.title('Price Histogram')

    return plt.figure

def plot_price_historgam_subplot(df):
    '''
    Returns subplot with price histogram. The first with full range of prices and the second
    with values up to 60000.
    '''

    fig, ax = plt.subplots(1, 2, figsize=[16, 5])

    binsize = 1000
    bins = np.arange(0, df.price.max()+binsize, binsize)

    ax[0].hist(data = df, x = 'price', bins = bins)
    ax[0].set(ylabel= 'Frequency', xlabel='Price (£)')

    ax[1].hist(data = df, x = 'price', bins = bins)
    ax[1].set(ylabel= 'Frequency', xlabel='Price (£)')
    ax[1].set_xlim(0, 60000);
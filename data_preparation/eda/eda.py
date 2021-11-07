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

    X = get_label_encoding_for_categoricals(X)

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

def plot_eda_subplot1(df):
    '''
    Returns a group of plots of variables vs price.
    '''

    fig, ax = plt.subplots(2, 3, figsize=[24, 15])
    alpha = 0.5
    
    # fig 1
    ax[0,0].scatter(df.length, df.price, alpha=alpha)
    ax[0,0].set(ylabel= 'Price (£)', xlabel='Length (mm)')

    # fig 2
    ax[0,1].scatter(df.boot_space_seats_down, df.price, alpha=alpha)
    ax[0,1].set(ylabel= 'Price (£)', xlabel='Boot Space (L)')
    ax[0,1].scatter(df.boot_space_seats_up, df.price, alpha=alpha)
    ax[0,1].set_xlim(0, 3000)
    ax[0,1].legend(['Seats Down', 'Seats Up'], loc="upper right")

    # fig 3
    ax[0,2].scatter(df.wheelbase, df.price, alpha=alpha)
    ax[0,2].set(ylabel= 'Price (£)', xlabel='Wheelbase (mm)')

    # fig 4
    ax[1,0].scatter(df.width, df.price, alpha=alpha)
    ax[1,0].set(ylabel= 'Price (£)', xlabel='Height (mm)')

    # fig 5
    ax[1,1].scatter(df.manufactured_year, df.price, alpha=alpha)
    ax[1,1].set(ylabel= 'Price (£)', xlabel='Manufactured Year')

    # fig 6
    ax[1,2].scatter(df.engine_power, df.price, alpha=alpha)
    ax[1,2].set(ylabel= 'Price (£)', xlabel='Engine Power (bhp)');
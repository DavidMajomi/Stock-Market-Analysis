
# Data Manipulation
import pandas as pd
import math
from datetime import datetime
import statistics
import numpy as np
# Data Vizualization
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import mean_absolute_error

# Arima Model Building
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA


# LSTM Model Building
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers
from keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler


from get_stock_data import get_all_price_data_mapped_to_ticker


map = get_all_price_data_mapped_to_ticker()
for x in map:
    map[x]['Date'] = pd.to_datetime(map[x]['Date'])
    map[x].set_index("Date", inplace = True)    



def get_range(df, start, end):
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    df = df.loc[start:end]
    
    # Multivariate
    # df = df[["Close", "Volume"]]

    
    # Univariate
    df = df[["Close"]]

    # Creates new columns
    for x in range(1, 5 + 1):            
        df[f"target - {x}"] = df["Close"].shift(x)
        
    df.dropna(inplace = True)
     
    return df


def seperate_df(df):
    dates = df.index  
    X = df.iloc[:, 1:]
    X = X.iloc[:, ::-1]
    Y = df[["Close"]]

    return dates, X, Y


def set_scalers(X, y):
    global y_scaler
    scaler = MinMaxScaler(feature_range=(-1, 1))
    scaler.fit(X)
    X = scaler.transform(X)
    
    y_scaler = MinMaxScaler(feature_range=(0, 1))
    y_scaler.fit(y)
    y = y_scaler.transform(y)
    return X, y


def create_split(X, y, dates):
    global q_80, q_90, dates_train, X_train, y_train, dates_val, X_val, y_val, dates_test, X_test, y_test
    
    q_80 = int(len(dates) * .8)
    q_90 = int(len(dates) * .9)
    
    dates_train, X_train, y_train = dates[:q_80], X[:q_80], y[:q_80]
    
    dates_val, X_val, y_val = dates[q_80:q_90], X[q_80:q_90], y[q_80:q_90]
    dates_test, X_test, y_test = dates[q_90:], X[q_90:], y[q_90:]


#%%
    


def simulate_model(ticker):
    global model
    global df
    df = get_range(map[ticker], "1-1-2023", "12-31-2024")
    dates, X, y = seperate_df(df)
    
    
    # Implement Scaler
    X, y = set_scalers(X, y)
    
    # Create train, val, and test split
    create_split(X, y, dates)
    print(len(y_test), len(X_test))
    model = Sequential([layers.LSTM(256, return_sequences = True, input_shape=(X_train.shape[1],1)),
        layers.Dropout(.3),
        layers.LSTM(256),
        layers.Dense(128),
        layers.Dense(64),
        layers.Dense(1)])
    
    
    
    
    model.compile(loss='mse', 
                  optimizer=Adam(learning_rate=0.001),
                  metrics=['mean_absolute_error'])
    
    model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs = 75)
    test_predictions = model.predict(X[-5].reshape(1,5))
    next_day_pred = y_scaler.inverse_transform(test_predictions)

    if dates[-1].dayofweek == 4:
        next_day = dates[-1]+ pd.Timedelta("3 day")
    else:
        next_day = dates[-1]+ pd.Timedelta("1 day")
    
    return next_day_pred, next_day
    
    

#%%










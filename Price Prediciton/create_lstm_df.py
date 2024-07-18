# Data Manipulation
import pandas as pd
import math
from datetime import datetime

days_back = 4

def get_range(df, start, end):
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    df = df.loc[start:end]
    
    # Univariate but will change to multivariate
    df = df[["Close"]]

    # Creates new columns
    for x in range(1, n + 1):            
        df[f"target - {x}"] = df["Close"].shift(x)

    
    
    
    # df["target - 1"] = df["Close"].shift(1)
    # df["target - 2"] = df["Close"].shift(2)
    # df["target - 3"] = df["Close"].shift(3)
    
    
    
    df.dropna(inplace = True)
     
    return df


def seperate_df(df):
    dates = df.index  
    X = df.iloc[:, 1:n + 1]
    Y = df["Close"]

    return dates, X, Y

df = get_range(map["HD"], "1-1-2023", "12-31-2024")

dates, X, y = seperate_df(df)


X = X.to_numpy()
X = X.reshape(len(dates), X.shape[1], 1)
    

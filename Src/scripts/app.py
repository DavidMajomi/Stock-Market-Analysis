import os
import time
import secrets
import sqlite3
import datetime
import random
import pandas as pd
import multiprocessing
from dotenv import load_dotenv

import init_all_data
import path_constants
import get_stock_data
import price_prediction
import server_client_constants

from pathlib import Path
from flask import Flask
from flask_cors import CORS
from sqlalchemy import create_engine
from path_constants import PATH_TO_DB_PRICE_DATA, PATH_TO_DB_WITH_MODEL_PREDICTIONS


os.chdir(os.path.dirname(os.path.abspath(__file__)))


app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = secrets.token_bytes(16) 

LOCK = multiprocessing.Lock()

ALL_TICKERS_IN_DB_DICT = get_stock_data.get_tickers_as_associative_container(path_constants.PATH_TO_DB_PRICE_DATA)
ALL_TICKER_DATA = {}


def get_historical_price_data(ticker: str) -> tuple[list, list]:
    table = get_stock_data.get_table_matching_ticker(ticker)
    # print(table.to_dict())
    
    return table.columns.values.tolist(), table.values.tolist()


def get_todays_predicted_close_price(ticker):
    print("USE DB Pred")
    print(ticker)
    query = f""" SELECT todays_predicted_close_price 
    FROM {path_constants.PREDICTIONS_TABLE_NAME}
    WHERE ticker='{ticker}';"""
    connection = sqlite3.connect(path_constants.PATH_TO_DB_WITH_MODEL_PREDICTIONS)
    
    cursor = connection.cursor()
    
    cursor.execute(query)
    data = cursor.fetchall()
    
    return data[0][0]
   
    
def get_predicted_price_movement_score(ticker: str) -> int:
    
    return 0


def get_adjusted_close_price_based_on_sentiment(ticker: str) -> float:
    return 1000
    
    
def get_ticker_info(ticker : str) -> dict:
    if (ticker in ALL_TICKER_DATA):
        
        ticker_data_to_return_to_client = {
            "ticker" : ticker,
            "todays_predicted_close_price": ALL_TICKER_DATA[ticker]["todays_predicted_close_price"],
            "historical_price_data" : ALL_TICKER_DATA[ticker]["historical_price_data"],
            "predicted_price_movement_score" : ALL_TICKER_DATA[ticker]["predicted_price_movement_score"],
            "adjusted_close_price_based_on_sentiment" : ALL_TICKER_DATA[ticker]["adjusted_close_price_based_on_sentiment"]
        }
            
    else:
        data_columns, hist_data = get_historical_price_data(ticker)
        
        ticker_data_to_return_to_client = {
            "ticker" : ticker,
            "todays_predicted_close_price": get_todays_predicted_close_price(ticker),
            "historical_price_data" : hist_data,
            "predicted_price_movement_score" : get_predicted_price_movement_score(ticker),
            "adjusted_close_price_based_on_sentiment" : get_adjusted_close_price_based_on_sentiment(ticker)
        }
        
        
        ticker_data_to_cache = ticker_data_to_return_to_client
        ticker_data_to_cache["historical_price_columns"] = data_columns
            
        LOCK.acquire()
        ALL_TICKER_DATA[ticker] = ticker_data_to_cache
        LOCK.release()
        
    return ticker_data_to_return_to_client
    
    
def load_all_s_and_p_data_to_memory():
    list_of_tickers = get_stock_data.get_list_of_tickers_in_db(PATH_TO_DB_PRICE_DATA)
    
    count = 0
    for ticker in list_of_tickers:
        print(count)
        data_columns, hist_data = get_historical_price_data(ticker)
        
        ticker_data = {
            "ticker" : ticker,
            "todays_predicted_close_price": get_todays_predicted_close_price(ticker),
            "historical_price_columns" : data_columns,
            "historical_price_data" : hist_data,
            "predicted_price_movement_score" : get_stock_data.get_pred_price_mov_score(ticker),
            "adjusted_close_price_based_on_sentiment" : get_stock_data.get_pred_price_mov_score(ticker)
        }
        
        ALL_TICKER_DATA[ticker] = ticker_data
        
        count += 1
        
        
def process_request(request_data):

    if "get_available_tickers" in request_data:
        bool_get_available_tickers = request_data["get_available_tickers"]
    else:
        bool_get_available_tickers = False
        
        
    if "ticker" in request_data:
        ticker = request_data["ticker"]
    else:
        ticker = None
        
    
    if (ticker in ALL_TICKERS_IN_DB_DICT):
        
        meta_data = {
            "Status" : 200,
            "ticker" : "Stock ticker",
            "todays_predicted_close_price": "Predicted closing price of ticker",
            "historical_price_data" : "Historical data in format ",
            "predicted_price_movement_score" : "A score based on market sentiment from news analysis",
            "adjusted_close_price_based_on_sentiment" : "Closing price adjusted for sentiment",
            "available_tickers" : "Not Requested",
            "Issue" : None
        }
        
        
        if (ticker in ALL_TICKER_DATA):
            print("Ticker in dict")
            
            meta_data["historical_price_data"] = f"Historical data in format {ALL_TICKER_DATA[ticker]['historical_price_columns']}"
            
            ticker_data_to_return_to_client = get_ticker_info(ticker)
                
        else:
            data_columns, hist_data = get_historical_price_data(ticker)
            
            meta_data["historical_price_data"] = f"Historical data in format {data_columns}"
            
            ticker_data_to_return_to_client = get_ticker_info(ticker)
            
            
    elif (bool_get_available_tickers == True):
        meta_data = {
            "Status" : 200,
            "ticker" : "Stock ticker",
            "todays_predicted_close_price": "Predicted closing price of ticker",
            "historical_price_data" : "Not requested",
            "predicted_price_movement_score" : "A score based on market sentiment from news analysis",
            "adjusted_close_price_based_on_sentiment" : "Closing price adjusted for sentiment",
            "available_tickers" : "",
            "Issue" : None
        }
        
        ticker_data_to_return_to_client = None
        
    else:
        meta_data = {
            "Status" : 400,
            "ticker" : "Stock ticker",
            "todays_predicted_close_price": "Predicted closing price of ticker",
            "historical_price_data" : "Historical data in format ",
            "predicted_price_movement_score" : "A score based on market sentiment from news analysis",
            "adjusted_close_price_based_on_sentiment" : "Closing price adjusted for sentiment",
            "available_tickers" : "Not Requested",
            "Issue" : "Bad ticker info"
        }
        
        ticker_data_to_return_to_client = None
        
    
    if bool_get_available_tickers == True:
        meta_data["available_tickers"] = list(ALL_TICKERS_IN_DB_DICT)
        
                       
    data_to_send = {
        "Meta Data" : meta_data,
        "Ticker Data" : ticker_data_to_return_to_client
    }
    
    return data_to_send


def train_models_and_store_predictions():
    all_ticker_data = []
    list_of_tickers = get_stock_data.get_list_of_tickers_in_db(PATH_TO_DB_PRICE_DATA)
    print(f"List of tickers: {list_of_tickers}")
    
    count = 0
    for ticker in list_of_tickers:
        t1 = time.perf_counter()
        next_day_pred, date, error = price_prediction.simulate_model(ticker)
        t2 = time.perf_counter()
        next_day_pred = float(next_day_pred[0])
        print(count)
        
        ticker_data = {
            "ticker" : ticker,
            "todays_predicted_close_price": next_day_pred,
            "price_prediction_date" : date,
            "price_prediction_mean_absolute_percentage_error" : round(error * 100, 3),
            "predicted_price_movement_score" : get_predicted_price_movement_score(ticker),
            "adjusted_close_price_based_on_sentiment" : get_adjusted_close_price_based_on_sentiment(ticker),
            "price_prediction_train_pred_time" : (t2 - t1)
        }
        
        all_ticker_data.append(ticker_data)
        
        count += 1
        
    predictions_df = pd.DataFrame.from_records(all_ticker_data)
    
    print(predictions_df)
    
    engine = create_engine("sqlite:///" + path_constants.PATH_TO_DB_WITH_MODEL_PREDICTIONS, echo=False)
        
    predictions_df.to_sql(path_constants.PREDICTIONS_TABLE_NAME, con=engine, if_exists="replace", index=False)
    
    engine.dispose()
    
    
def generate_demo_price(ticker):
    price_data = float(get_stock_data.get_most_recent_price(ticker))
    print(price_data)
    
    num = random.random()
    
    if num < 0.5:
        pred = price_data + (price_data * 0.02)
    else:
        pred = price_data - (price_data * 0.02)
        
    pred = price_data
    date = str(datetime.datetime.now())
    error = 0.02
    
    return [pred], date, error


def generate_price_movement_score(demo_price):
    
    num = random.random()
    
    if num < 0.5:
        pred = demo_price + (demo_price * 0.02)
    else:
        pred = demo_price - (demo_price * 0.02)
    
    return pred
    
    
def generate_and_store_demo_model_predictions():
    
    all_ticker_data = []
    list_of_tickers = get_stock_data.get_list_of_tickers_in_db(PATH_TO_DB_PRICE_DATA)
    # print(f"List of tickers: {list_of_tickers}")
    
    count = 0
    for ticker in list_of_tickers:
        # if ticker != "BRK.B" and ticker != "BF.B":
        t1 = time.perf_counter()
        next_day_pred, date, error = generate_demo_price(ticker)
        t2 = time.perf_counter()
        next_day_pred = float(next_day_pred[0])
        # print(f"{ticker}: {count}")
        
        ticker_data = {
            "ticker" : ticker,
            "todays_predicted_close_price": next_day_pred,
            "price_prediction_date" : date,
            "price_prediction_mean_absolute_percentage_error" : round(error * 100, 3),
            "predicted_price_movement_score" : generate_price_movement_score(next_day_pred),
            "adjusted_close_price_based_on_sentiment" : next_day_pred,
            "price_prediction_train_pred_time" : (t2 - t1)
        }
        
        all_ticker_data.append(ticker_data)
        
        count += 1
        
    predictions_df = pd.DataFrame.from_records(all_ticker_data)
    
    # print(predictions_df)
    
    engine = create_engine("sqlite:///" + path_constants.PATH_TO_DB_WITH_MODEL_PREDICTIONS, echo=False)
        
    predictions_df.to_sql(path_constants.PREDICTIONS_TABLE_NAME, con=engine, if_exists="replace", index=False)
    
    engine.dispose()



def check_required_data_exists():
    
    return (len(get_stock_data.get_list_of_tickers_in_db(PATH_TO_DB_PRICE_DATA)) > 2)
    
    
def check_predictions_exist():
    path = Path(PATH_TO_DB_WITH_MODEL_PREDICTIONS)
    
    return path.is_file()



def testing_mode_startup():
    required_data_exists = check_required_data_exists()
    if required_data_exists:
        print("Required Data Present")
    else:
        init_all_data.init_all_required_data()
    
    predictions_exist = check_predictions_exist()
    if predictions_exist:
        print("Prediction Data Exists")
    else:
        generate_and_store_demo_model_predictions()
    
    
def update_data():
    
    true_false_dict = {
        "True" : True,
        "TRUE" : True,
        "true" : True,
        "False" : False,
        "FALSE" : False,
        "false" : False
    }
    
    load_dotenv(override=True)
    testing_mode = true_false_dict[os.getenv("TESTING_MODE")]
    time_to_update = int(os.getenv("UPDATE_HOUR"))
    
    
    while True:
        current_time = datetime.datetime.now()
        
        if not testing_mode:
            # Wait until new day before updating data
            while not current_time.hour == time_to_update:
                current_time = datetime.datetime.now()
                
                load_dotenv(override=True)
                
                time_to_update = int(os.getenv("UPDATE_HOUR"))
                time.sleep(3600)
        
            init_all_data.init_all_required_data()
            train_models_and_store_predictions()
            time.sleep(3600)            
                
        else:
            # Wait until new day before updating data
            while not current_time.hour == time_to_update:
                current_time = datetime.datetime.now()
                
                load_dotenv(override=True)
                                
                time_to_update = int(os.getenv("UPDATE_HOUR"))

                time.sleep(3600)
        
            testing_mode_startup()
            time.sleep(3600)            
                
            


@app.route("/", methods = ['GET'])
@app.route("/get_available_tickers", methods = ['GET'])
def get_available_tickers():
    data = {"get_available_tickers" : True}
    
    return process_request(data)


@app.route('/get_data/<string:ticker>', methods = ['GET'])
def allow(ticker):
    
    data = {"ticker" : ticker, "get_available_tickers" : False}
    
    return process_request(data)


if __name__ == '__main__':
    
    true_false_dict = {
        "True" : True,
        "TRUE" : True,
        "true" : True,
        "False" : False,
        "FALSE" : False,
        "false" : False
    }
    
    load_dotenv(override=True)
    testing_mode = true_false_dict[os.getenv("TESTING_MODE")]
    print(f"Testing Mode: {testing_mode}")
    
    if testing_mode is False:
        init_all_data.init_all_required_data()
        train_models_and_store_predictions()
    else:
        testing_mode_startup()
    
    
    load_all_s_and_p_data_to_memory()
    ALL_TICKERS_IN_DB_DICT = server_client_constants.ALL_TICKERS_IN_DB_DICT
    
    
    app.run(host='0.0.0.0', port=5000, debug = True)

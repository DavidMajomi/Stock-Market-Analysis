import secrets
import os
import server
from flask import Flask

import server_client_constants

os.chdir(os.path.dirname(os.path.abspath(__file__)))

HEADER = server_client_constants.HEADER
PORT = server_client_constants.PORT
SERVER = server_client_constants.SERVER
ADDR = server_client_constants.ADDR
FORMAT = server_client_constants.FORMAT


app = Flask(__name__)

app.config['SECRET_KEY'] = secrets.token_bytes(16) 

ALL_TICKERS_IN_DB_DICT = None
ALL_TICKER_DATA = {}

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
            "historical_price_data" : f"Historical data in format ",
            "predicted_price_movement_score" : "A score based on market sentiment from news analysis",
            "adjusted_close_price_based_on_sentiment" : "Closing price adjusted for sentiment",
            "available_tickers" : "Not Requested",
            "Issue" : None
        }
        
        
        if (ticker in ALL_TICKER_DATA):
            print("Ticker in dict")
            
            meta_data["historical_price_data"] = f"Historical data in format {ALL_TICKER_DATA[ticker]['historical_price_columns']}"
            
            ticker_data_to_return_to_client = server.get_ticker_info(ticker)
                
        else:
            data_columns, hist_data = server.get_historical_price_data(ticker)
            
            meta_data["historical_price_data"] = f"Historical data in format {data_columns}"
            
            ticker_data_to_return_to_client = server.get_ticker_info(ticker)
            
            
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
            "historical_price_data" : f"Historical data in format ",
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
    server.init_all_required_data()
    # server.load_all_s_and_p_data_to_memory()
    ALL_TICKERS_IN_DB_DICT = server_client_constants.ALL_TICKERS_IN_DB_DICT
    
    
    app.run(host='0.0.0.0', port=5000, debug = True)

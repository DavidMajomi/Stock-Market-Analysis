import os
import json
import socket
import time
import threading
import server_client_constants
import multiprocessing
from path_constants import PATH_TO_DB_PRICE_DATA  
from init_all_data import init_all_required_data
from get_stock_data import get_table_matching_ticker, get_list_of_tickers_in_db
from price_prediction import simulate_model

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Network related constants
HEADER = server_client_constants.HEADER
PORT = server_client_constants.PORT
SERVER = server_client_constants.ADDR
ADDR = server_client_constants.ADDR
FORMAT = server_client_constants.FORMAT

LOCK = multiprocessing.Lock()

ALL_TICKERS_IN_DB_DICT = server_client_constants.ALL_TICKERS_IN_DB_DICT
ALL_TICKER_DATA = {}


def get_todays_predicted_close_price(ticker: str) -> float:
        
    next_day_pred, date, error = simulate_model(ticker)
    
    return float(next_day_pred[0])


def get_historical_price_data(ticker: str) -> list:
    table = get_table_matching_ticker(ticker)
    # print(table.to_dict())
    
    return table.columns.values.tolist(), table.values.tolist()


def get_predicted_price_movement_score(ticker: str) -> int:
    
    return 0


def get_adjusted_close_price_based_on_sentiment(ticker: str) -> float:
    return 1000


def load_all_s_and_p_data_to_memory():
    list_of_tickers = get_list_of_tickers_in_db(PATH_TO_DB_PRICE_DATA)
    
    count = 0
    for ticker in list_of_tickers:
        print(count)
        data_columns, hist_data = get_historical_price_data(ticker)
        
        ticker_data = {
            "ticker" : ticker,
            "todays_predicted_close_price": get_todays_predicted_close_price(ticker),
            "historical_price_columns" : data_columns,
            "historical_price_data" : hist_data,
            "predicted_price_movement_score" : get_predicted_price_movement_score(ticker),
            "adjusted_close_price_based_on_sentiment" : get_adjusted_close_price_based_on_sentiment(ticker)
        }
        
        ALL_TICKER_DATA[ticker] = ticker_data
        
        count += 1
    

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


def handle_client(conn, addr, num_connections_to_server):
    print(f"New Conection {addr} connected")
    
    msg_length = conn.recv(HEADER).decode(FORMAT)
    # conn.send("Message Recieved".encode(FORMAT))
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        
        # conn.send("Message Recieved".encode(FORMAT))
        
        
        data_to_use = json.loads(msg)
        data_to_send_to_client = process_request(data_to_use)
        
        data_to_return = json.dumps(data_to_send_to_client, indent = 2)
        data_to_return_size = str(len(data_to_return.encode(FORMAT)))
        
        conn.send(data_to_return_size.encode(FORMAT))
        conn.send(data_to_return.encode(FORMAT))
        
        conn.send(" Disconnected Successfully".encode(FORMAT))
            
            
    conn.close()
        

def start():
    print("Setting up server...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    
    t1 = time.perf_counter()
    
    # init_all_required_data()
    # load_all_s_and_p_data_to_memory()
    
    t2 = time.perf_counter()
    
    print(f"Time taken to initialize and load data to memory is {t2 - t1}")
    
    server.listen()
    print(f"Server is listening on {SERVER}")
    
    
    
    num_connections_to_server = 0
    while True:
        num_connections_to_server = num_connections_to_server + 1
        
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr, num_connections_to_server))
        thread.start()
        
        print(f"Number of Connections: {threading.active_count() - 1} \n")


print("Starting Server...... \n")
start()
    


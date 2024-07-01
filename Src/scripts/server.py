import json
import socket
import threading
import server_client_constants
from pathlib import Path
# from init_all_data import init_all_required_data
from get_stock_data import get_table_matching_ticker

PATH = str(Path.cwd())

# Network related constants
HEADER = server_client_constants.HEADER
PORT = server_client_constants.PORT
SERVER = server_client_constants.ADDR
ADDR = server_client_constants.ADDR
FORMAT = server_client_constants.FORMAT


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def get_todays_predicted_close_price(ticker: str) -> float:
    return 1000


def get_historical_price_data(ticker: str) -> list:
    table = get_table_matching_ticker(ticker)
    # print(table.to_dict())
    
    return table.columns.values.tolist(), table.values.tolist()


def get_predicted_price_movement_score(ticker: str) -> int:
    
    return 0


def get_adjusted_close_price_based_on_sentiment(ticker: str) -> float:
    return 1000


def process_request(request_data):
    ticker = request_data["ticker"]
    
    data_columns, hist_data = get_historical_price_data(ticker)
    
    meta_data = {
        "Status" : 200,
        "ticker" : "Stock ticker",
        "todays_predicted_close_price": "Predicted closing price of ticker",
        "historical_price_data" : f"Historical data in format {data_columns}",
        "predicted_price_movement_score" : "A score based on market sentiment from news analysis",
        "adjusted_close_price_based_on_sentiment" : "Closing price adjusted for sentiment"
    }
    
    ticker_data_to_return_to_client = {
        "ticker" : ticker,
        "todays_predicted_close_price": get_todays_predicted_close_price(ticker),
        "historical_price_data" : hist_data,
        "predicted_price_movement_score" : get_predicted_price_movement_score(ticker),
        "adjusted_close_price_based_on_sentiment" : get_adjusted_close_price_based_on_sentiment(ticker)
    }
    
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
        
    server.listen()
    print(f"Server is listening on {SERVER}")
    
    # init_all_required_data()
    
    num_connections_to_server = 0
    while True:
        num_connections_to_server = num_connections_to_server + 1
        
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr, num_connections_to_server))
        thread.start()
        
        print(f"Number of Connections: {threading.active_count() - 1} \n")


print("Starting Server...... \n")
start()
    


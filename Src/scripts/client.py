import os
import socket
import json
import time
import server_client_constants

os.chdir(os.path.dirname(os.path.abspath(__file__)))

HEADER = server_client_constants.HEADER
PORT = server_client_constants.PORT
SERVER = server_client_constants.SERVER
ADDR = server_client_constants.ADDR
FORMAT = server_client_constants.FORMAT


def send(msg):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    
    message = msg.encode(FORMAT)
    
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))    
    
    
    client.send(send_length)
    client.send(message)
    
    recieve_data_length = int(client.recv(2048).decode(FORMAT))
        
    recieved_json_data = client.recv(recieve_data_length).decode(FORMAT)
    # print(recieved_json_data)
    
    recieved_data = json.loads(recieved_json_data)
    
    return recieved_data


def get_data_to_send() -> dict:
    return {"ticker" : "AAPL"}
    # return {"get_available_tickers" : True}
    # return {"ticker" : "A", "get_available_tickers" : True
    # return {"ticker" : "MSFT", "get_available_tickers" : False}


data = get_data_to_send()

data = json.dumps(data)

t1 = time.perf_counter()
recieved_data = send(data)
t2 = time.perf_counter()

print(f"time for first call = {t2 - t1}")

t3 = time.perf_counter()
recieved_data = send(data)
t4 = time.perf_counter()

print(f"time for second call = {t4 - t3}")

recieved = (recieved_data)

# print(type(recieved))
print(recieved)
print(recieved["Meta Data"], "\n")
print("Ticker: ", recieved["Ticker Data"]["ticker"])
print(f"Todays predicted close price: {recieved['Ticker Data']['todays_predicted_close_price']}" )



# print(recieved_data["Ticker Data"])
# print(json.dumps((recieved_data["Meta Data"]), indent=4))
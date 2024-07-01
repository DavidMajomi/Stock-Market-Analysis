import socket
import json
import server_client_constants


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


def get_data_to_send() -> str:
    return {"ticker" : "A"}


data = get_data_to_send()

data = json.dumps(data)


recieved_data = send(data)

print(json.dumps((recieved_data), indent=4))
# print(recieved_data["Ticker Data"])
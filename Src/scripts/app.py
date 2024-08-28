import json
import socket
import secrets
import os
from client import send
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


@app.route("/", methods = ['GET'])
@app.route("/get_available_tickers", methods = ['GET'])
def get_available_tickers():
    data = {"get_available_tickers" : True}
    
    data = json.dumps(data)
    
    return send(data)


@app.route('/get_data/<string:ticker>', methods = ['GET'])
def allow(ticker):
    
    data = {"ticker" : ticker, "get_available_tickers" : False}
    
    data = json.dumps(data)
    
    return send(data)



if __name__ == '__main__':
    # app.run(debug = True)
    app.run(host='0.0.0.0', port=5000, debug = True)

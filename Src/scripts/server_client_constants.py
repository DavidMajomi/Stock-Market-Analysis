import socket
import path_constants
from get_stock_data import get_tickers_as_associative_container

# Network related constants
HEADER = 64
PORT = 8960
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
ALL_TICKERS_IN_DB_DICT = get_tickers_as_associative_container(path_constants.PATH_TO_DB_PRICE_DATA)
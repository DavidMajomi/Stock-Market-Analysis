import os
from get_stock_data import get_all_price_data_mapped_to_ticker

os.chdir(os.path.dirname(os.path.abspath(__file__)))

map = get_all_price_data_mapped_to_ticker()

keys = map.keys()

print(keys)

print(map["A"])
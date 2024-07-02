from get_stock_data import get_all_price_data_mapped_to_ticker

map = get_all_price_data_mapped_to_ticker()

keys = map.keys()

print(keys)

print(map["A"])
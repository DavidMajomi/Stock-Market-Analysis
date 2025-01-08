from init_all_data import init_all_required_data

init_all_required_data()

import os
from get_stock_data import get_all_price_data_mapped_to_ticker

# os.chdir(os.path.dirname(os.path.abspath(__file__)))
map = get_all_price_data_mapped_to_ticker()\

# Change index to datetime
for x in map:
    map[x]['Date'] = pd.to_datetime(map[x]['Date'])
    map[x].set_index("Date", inplace = True)    

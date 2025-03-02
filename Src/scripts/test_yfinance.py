import yfinance as yf
data = yf.Ticker("MSFT")

msft_data = data.info

# print(msft_data)
print(f"EBITDA: {msft_data['ebitda']}")
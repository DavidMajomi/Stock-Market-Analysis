from price_prediction import simulate_model

# Replace "AAPL" with Ticker

next_day_pred, date, error = simulate_model("AAPL")
print(date, next_day_pred, f"Mean Absolute Percentage Error = {round(error * 100, 3)}%")


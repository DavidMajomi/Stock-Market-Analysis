from price_prediction import simulate_model

next_day_pred, date = simulate_model("AAPL")
print(date, next_day_pred)

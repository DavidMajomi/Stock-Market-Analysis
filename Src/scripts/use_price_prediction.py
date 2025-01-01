from price_prediction import simulate_model
import time

t1 = time.perf_counter()
# Replace "AAPL" with Ticker
next_day_pred, date, error = simulate_model("AAPL")
t2 = time.perf_counter()

print(date, "\nPrice Prediction:", float(next_day_pred[0]), f"\nMean Absolute Percentage Error = {round(error * 100, 3)}%")
print(f"time for first call = {t2 - t1}")


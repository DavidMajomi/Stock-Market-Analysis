# Stock Market Analysis

## Overview
An Open source python server application for distributing public financial data and compute results on a local network, minimizing external requests, and conserving external API usage.

## Features
- Stock price scraping and storage using SQLite database
- Stock News gathering and sentiment analysis
- Local Flask server with CORS support for multi-process communications
- RESTful API endpoints for stock predictions and data access
- In-memory caching system for optimal performance
- LSTM-based price prediction using historical data
- Technical indicator calculations
- Support for all S&P 500 companies

## Directory Structure

### [Data](./data)
* [database/](./data/database) - Stores SQLite databases for:
  - Historical price data
  - Model predictions
  - Stock metadata
* [raw data/](./data/raw%20data/) - Contains raw data files before processing

### [Documentation](./Documentation)
* Contains team breakdowns, tasks and other relevant documentation
* [Current Project Scope](./Documentation/Project%20Scope.md)

### [Src](./Src)
* [notebooks/](./Src/scripts/notebooks) - Jupyter notebooks for data scraping
* [scripts/](./Src/scripts) - Core Python scripts including:
  - `app.py` - Main Flask application
  - `init_all_data.py` - Data initialization
  - `price_prediction.py` - LSTM model implementation
  - `get_stock_data.py` - Data retrieval utilities

## Setup

### Prerequisites
- Python 3.10+
- pip (Python package manager)
- Docker (optional, for containerized deployment)

### Installation

#### Local Development
1. Create and enable a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following variables:
```
NEWS_API_ORG_KEY = "API_KEY"    # Your News API key from newsapi.org
TESTING_MODE = "True"           # Enable testing mode with sample data and limited model training
                                # Set to "False" for production mode with live data
UPDATE_HOUR = 0                 # Hour to uupdate in 24 hour format
```

4. Initialize the data and train models:
```bash
cd Src/scripts
python init_all_data.py
python app.py
```

#### Docker Deployment
1. Build and run using Docker Compose:
```bash
docker compose up --build
```

The application will be available at `http://localhost:5000`

## REST API Usage

### Endpoints

#### Get Stock Information
```
GET /get_data/{ticker}
```

Response includes:
- Today's predicted close price
- Historical price data
- Predicted price movement score
- Sentiment-adjusted close price

Example Response:
```json
{
    "ticker": "AAPL",
    "todays_predicted_close_price": 178.45,
    "historical_price_data": [...],
    "predicted_price_movement_score": 0,
    "adjusted_close_price_based_on_sentiment": 180.25
}
```

#### Get Available Tickers
```
GET /get_available_tickers
```
Returns a list of all available S&P 500 tickers in the database.

## Implementation Details

### Data Storage
- Uses SQLite databases for storing historical prices and predictions
- Implements an in-memory cache for frequently accessed data
- Thread-safe data access using multiprocessing locks

### Model Training
- Automated model training pipeline
- Stores predictions in a dedicated SQLite database
- Updates predictions periodically with new market data

### Security
- Uses Flask's secret key for session management
- Implements CORS for controlled API access
- Runs as non-privileged user in Docker container

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Disclaimer
This application is for educational and research purposes only. Trading stocks carries risk, and predictions should not be used as the sole basis for investment decisions.

## License
MIT License

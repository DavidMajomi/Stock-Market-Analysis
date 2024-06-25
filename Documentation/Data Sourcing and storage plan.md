
# Data format (Depends on data frequency, assumed to be daily)
- #### Date 
- #### Opening price
- #### High Price
- #### Low Price
- #### Closing Price
- #### Volume Traded
- #### Adjusted Closing Price Data

# Data Sourcing
- ## Stock Price Data
    * Primary Data source is the yfinance api
        * It will be received as a pandas dataframe
    * Data will be collected iteratively for each stock ticker, and then stored in a database
    * The dataframe will be converted for storage using SQLAlchemy and stored as a table named after its ticker
    * A csv file containing tickers and listing dates both of which are needed to get relevant yfinance data has already been scraped from wikipedia

- ## News and Sentiment Data
    * Data Sources include:
        * Alpha Vantage



# Data Utilization

- ## The Format the Machine Learning Model requires

    * The model requires a pandas dataframe
    * Pandas can just drectly read the table and convert to dataframe using create_engine
    
- ### Each Stock will be represented as a standalone table in the database using it's ticker
    - This means the calling funtion will be responsible for accurately passing the name of the required stock preferrably using a ticker.
    - A central point of reference for all tickers would be preferred to avoid naming issues
    - Calling functions will be responsible for exception handling

- ## The Format the web app requires
    - TBD

- # Machine Learning Model storage
    - TBD
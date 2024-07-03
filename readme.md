# Stock Market Analysis

## Overview
The goal of this project is to analyze the S&P 500 index and create an interactive frontend to utilize the meaningful insights gained using Machine Learning.

## Current Tasks
- ### Machine Learning 
    - Price prediction with LSTM
    - Sentiment Analysis

- ### A python server to provide required data to different clients

- ### Building a web app to display data using data from server
    - TBD


- ### Data Sourcing and storage
    - News Data for sentiment analysis


## Completed tasks
- ### Data Sourcing and storage
    * Getting s&p index tickers 
    * Getting and storing historical stock prices for all tickers in a database.


## Roles
- ### Price prediction with LSTM
    * Jaydentani
    * Chtjigur
    * Brianna
    
- ### Price movement prediction with sentiment analysis
    * Dagi
    * Ana
    * King

- ### Data Sourcing and Storage
    * TBD
    * TBD

- ### Web app
    * Due to the scope, i think everyone will probably work here at some point.

- ### Python Server and related API's
    * David

## Directory Structure

### [Data](./data)

* [database/](./data/database)
* [raw data/](./data/raw%20data/)


### [Documentation](./Documentation)

* Contains team breakdowns, tasks and other relevant stuff.
* [Current Project Scope](./Documentation/Project%20Scope.md)


### [Src](.\Src)

* [notebooks/](./Src/notebooks)
* [scripts/](./Src/scripts)

## Setup

* TBD
- ### General setup requirement
    * Create and enable a python venv
    * Install requirements from the requirements.txt file
- ### Getting Data
    * Run the init_all_data.py file from the scripts directory. This will automatically get the required data for price prediction using LSTM.

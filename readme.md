# Stock Market Analysis

## Overview
An Open source python server application for distributing public financial data and compute results on a local network, minimizing external requests, and conserving external API usage.

## Features
- Stock price scraping and storage
- Stock News gathering scraping and API's and storage
- A local server for multi-process communications
- A flask endpoint for easier data sharing and access
- A plug and play design for seamless feature integration
- A functional LSTM price prediction feature using acquired historical prices.

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
    * Run the setup.py file from the scripts directory. This will automatically get the required data for price prediction using LSTM.
    * Enter required api keys to automatically store them in related files

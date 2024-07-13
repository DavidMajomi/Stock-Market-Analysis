from init_all_data import init_all_required_data
import path_constants

PATH_TO_ALPHAVANTAGE_API_KEY = path_constants.PATH_TO_ALPHAVANTAGE_API_KEY 
PATH_TO_NEWS_API_ORG_API_KEY = path_constants.PATH_TO_NEWS_API_ORG_API_KEY
PATH_TO_GUARDIAN_NEWS_API_KEY = path_constants.PATH_TO_GUARDIAN_NEWS_API_KEY

ALPHAVANTAGE_API_KEY_FILE_NAME = path_constants.ALPHAVANTAGE_API_KEY_FILE_NAME
NEWS_API_ORG_API_KEY_FILE_NAME = path_constants.NEWS_API_ORG_API_KEY_FILE_NAME
GUARDIAN_NEWS_API_KEY_FILE_NAME = path_constants.ALPHAVANTAGE_API_KEY_FILE_NAME

def output_api_key(key, file):
    f = open(file, "w")
    f.write(key)
    f.close()
        
        
def setup_api_keys():
    key = input("Enter your Guardian News API key: ")
    output_api_key(key, file=PATH_TO_GUARDIAN_NEWS_API_KEY)
    

setup_api_keys()
init_all_required_data()
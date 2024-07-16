from init_all_data import init_all_required_data
import path_constants

PATH_TO_ALPHAVANTAGE_API_KEY = path_constants.PATH_TO_ALPHAVANTAGE_API_KEY 
PATH_TO_NEWS_API_ORG_API_KEY = path_constants.PATH_TO_NEWS_API_ORG_API_KEY
PATH_TO_GUARDIAN_NEWS_API_KEY = path_constants.PATH_TO_GUARDIAN_NEWS_API_KEY

ALPHAVANTAGE_API_KEY_FILE_NAME = path_constants.ALPHAVANTAGE_API_KEY_FILE_NAME
NEWS_API_ORG_API_KEY_FILE_NAME = path_constants.NEWS_API_ORG_API_KEY_FILE_NAME
GUARDIAN_NEWS_API_KEY_FILE_NAME = path_constants.ALPHAVANTAGE_API_KEY_FILE_NAME


def int_entered_is_valid_option(num_entered, min_option, max_option):
    if (not num_entered.isdigit()):
        return False
    
    if(int(num_entered) >= min_option and int(num_entered) <= max_option):
        return True
    else:
        return False

def output_api_key(key, file):
    f = open(file, "w")
    f.write(key)
    f.close()
        
        
def setup_api_keys():
    
    valid = False
    while (valid == False):
    
        print("Api Setup here are you options: ")
        print("1.) Setup Guardian News API key")
        print("2.) Setup newsapi.org key")
        print("3.) Setup all of the above")
        
        response = (input("Choose from the options: "))
        
        valid = int_entered_is_valid_option(response, 1, 3)
        
        if (valid == False):
            print("Invalid Response \n\n")
        else:
            response = int(response)
        
        
    if (response == 1):
        key = input("Enter your Guardian News API key: ")
        file = PATH_TO_GUARDIAN_NEWS_API_KEY
        output_api_key(key, file)
        
    elif (response == 2):
        key = input("Enter newsapi.org API key: ")
        file - PATH_TO_NEWS_API_ORG_API_KEY
        output_api_key(key, file)
        
    elif (response == 3):
        key = input("Enter newsapi.org API key: ")
        file = PATH_TO_NEWS_API_ORG_API_KEY
        output_api_key(key, file) 
        
        key = input("Enter your Guardian News API key: ")
        file = PATH_TO_GUARDIAN_NEWS_API_KEY
        output_api_key(key, file) 
    
    

# setup_api_keys()
init_all_required_data()
import os
import pandas as pd
import path_constants

os.chdir(os.path.dirname(os.path.abspath(__file__)))

PATH_TO_CSV_WITH_S_AND_P_DATA = path_constants.PATH_TO_CSV_WITH_S_AND_P_DATA

def get_s_and_p_info():
    
    link = (
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks"
    )
    df = pd.read_html(link, header=0)[0]

    # Write to CSV
    df.to_csv(PATH_TO_CSV_WITH_S_AND_P_DATA, index=False)
#Import libraries
import os
import requests
import json
import pandas as pd
from datetime import datetime

#Set global variables
fpath = "/Users/chuying/Documents/dataeng_assessment/q4/"
new_df = pd.DataFrame()

#Define endpoint
URL = "https://api.covid19api.com/live/country/singapore"

#Read data from endpoint into a dataframe
def read_json(endpoint):
    response = requests.get(URL)
    if response.status_code == 200: #200 means okay
        json_data = json.loads(response.content.decode('utf-8'))
        print(json_data)
        #print(type(data)) #returns a list
        df = pd.DataFrame.from_dict(json_data, orient='columns') #convert list to df
        df.columns = [x.lower() for x in df.columns] #set column headers to loweracse
        df = df.loc[:,'confirmed':'date'] #Extract relevant columns
    return(df)

#Get daily increase for specific columns
def get_daily_diffence(df,column_name):

    prev_col_name = "prev_" + column_name
    diff_col_name = "daily_diff_in_" + column_name

    df[prev_col_name] = df[column_name].shift().astype('Int64')
    df[diff_col_name] = df[column_name] - df[prev_col_name]

    return(df)

def split_datetime(new_df):

    #Convert datetime to date
    new_df['date'] = pd.to_datetime(new_df['date']).dt.date

    new_df.insert(0,'Year',pd.DatetimeIndex(new_df['date']).year)
    new_df.insert(1,'Month',pd.DatetimeIndex(new_df['date']).month)
    new_df.insert(2,'Day',pd.DatetimeIndex(new_df['date']).day)

    return(new_df)

def main():

    try:

        os.chdir(fpath)     # Change the current working directory
        print("Current working dir: ", os.getcwd())

        read_df = read_json(URL)
        print(read_df.dtypes)
        print(read_df.columns)

        #Calculate increase in confirmed cases
        new_df = get_daily_diffence(read_df, 'confirmed')
        new_df = get_daily_diffence(new_df, 'deaths')
        new_df = get_daily_diffence(new_df, 'recovered')
        #print(new_df)

        new_df.dropna(subset = ["prev_confirmed"], inplace=True) #drop first row with no prev value

        final_df = split_datetime(new_df)
        print(final_df)

        final_df.to_csv('cleansed_covid_data.csv', index=False)

    except:
        print("Error in code, please debug.")

if __name__ == '__main__':
    main()

#Direct read data from json file
# with open('/Users/chuying/Documents/dataeng_assessment/q2/response.json') as json_file:
#     data = json.load(json_file)
# print(data)

#Import libraries
import requests
import json
import pandas as pd

#Define endpoint
URL = "https://api.covid19api.com/live/country/singapore"

#Read data from endpoint
response = requests.get(URL)
if response.status_code == 200: #200 means okay
    json_data = json.loads(response.content.decode('utf-8'))
    print(json_data)
    #print(type(data)) #returns a list

#Direct read data from json file
# with open('/Users/chuying/Documents/dataeng_assessment/q2/response.json') as json_file:
#     data = json.load(json_file)
# print(data)

#Read json data into dataframe
read_df = pd.DataFrame.from_dict(json_data, orient='columns')
df = read_df[['Date','Confirmed','Deaths','Recovered','Active']]
df.insert(0,'Year',pd.DatetimeIndex(df['Date']).year)
df.insert(1,'Month',pd.DatetimeIndex(df['Date']).month)
df.insert(2,'Day',pd.DatetimeIndex(df['Date']).day)
df.drop(columns = ['Date'], inplace = True)

print(df)
df.to_csv('/Users/chuying/Documents/dataeng_assessment/q2/cleansed_covid_data.csv', index=False)

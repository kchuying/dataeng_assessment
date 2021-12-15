#import libraries
from os import listdir
from os.path import isfile, join
import os
import csv
import glob
import pandas as pd

#Set global variables
fpath = "/Users/chuying/Documents/dataeng_assessment/q1/"
combined_df = pd.DataFrame()

#Create functions
def read_csv_file(fpath):

    global combined_df #read, write global variable within a function

    #Lookup files in folder with specific prefix
    folder_dir = fpath + "dataset*.csv"
    csv_files = glob.glob(folder_dir, recursive=False)

    if len(csv_files) == 0:
        print("Files do not exist.")

    else:
        print("Files are found. Start reading files..")

        for fn in csv_files:
            print("File Path: ", fn)
            df = pd.read_csv(fn)

            check_for_nan = df['name'].isnull().sum()
            print("No of nulls in name column:",check_for_nan)

            combined_df = combined_df.append(pd.DataFrame(df), ignore_index=True) #ignore_index set to True for incremental binding
            combined_df.dropna(subset = ["name"], inplace=True) #drop rows without names

        #convert price to float data type
        combined_df['price'] = pd.to_numeric(combined_df["price"], downcast="float")
        return(combined_df)

def remove_keyword(df):
    salutation = ['Mr','Ms','Miss','Mrs','Dr'] #with dot
    salutation2 = ['MD','DDS','PhD'] #without dot

    keywords = r'\b(?:{})\b[^\w\s]'.format('|'.join(salutation))
    keywords2 = r'\b(?:{})\b'.format('|'.join(salutation2))

    df['name_cleaned'] = df['name'].str.replace(keywords, '', regex=True).str.strip()
    df['name_cleaned'] = df['name_cleaned'].str.replace(keywords2, '', regex=True).str.strip()

    return(df)

def split_name(row):
    name_list = row.split(' ')
    #print("Before Processing:" + str(name_list))
    name_length = len(name_list)

    if(name_length == 2):
        first_name = name_list[0]
        last_name = name_list[1]

    elif(name_length > 2):
        #assuming firstname contains everything except last element in list
        name_list[0:name_length-1] = [' '.join(name_list[0: name_length-1])]
        first_name = name_list[0]
        last_name = name_list[1]

    else:
        #Assuming the only name is firstname
        first_name = name_list[0]
        last_name = "Unknown"

    return(first_name, last_name)

def check_price(df):
    #create new column to check if price is above 100
    df['above_100'] = df['price'].apply(lambda x: 'True' if x >100 else 'False')
    return(df)

def main():

    try:

        os.chdir(fpath)     # Change the current working directory
        print("Current working dir: ", os.getcwd())

        #Read all csv files in folder path
        combined_df = read_csv_file(fpath)

        #Check data statistics
        desc =  combined_df.describe()
        print(desc)

        #Remove salutation from name column
        combined_df = remove_keyword(combined_df)

        #Split names into 2 columns
        for idx, row in combined_df.iterrows():
            #print(row.name_cleaned)
            split_res = split_name(row['name_cleaned']) #returns a tuple
            combined_df.at[idx, 'first_name'] = split_res[0]
            combined_df.at[idx, 'last_name'] = split_res[1]

        combined_df.drop(['name_cleaned'], axis = 1, inplace = True)

        #Check price value
        final_df = check_price(combined_df)
        print(final_df)

        #Write output to csv file
        final_df.to_csv('cleansed_data.csv', index=False)

    except FileNotFoundError:
        print("Directory: {0} does not exist".format(fpath))
    except NotADirectoryError:
        print("{0} is not a directory".format(fpath))
    except PermissionError:
        print("You do not have permissions to change to {0}".format(fpath))
    except OSError:
        print ("Can't change working directory")
    except:
        print("Error in code, please debug.")

if __name__ == '__main__':
    main()

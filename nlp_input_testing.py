import pandas as pd
import os


dataset = pd.read_excel('/Users/dbjt_baki/Desktop/Data_Engineering/Metathon/METATHON/nlp_input.xlsx',sheet_name='nlp_input')

dataset["User_Input"] = dataset["User_Input"].str.replace('.','')
dataset["Robo_response"] = dataset['Robo_response'].str.replace('.','')

delimiter = '.'  # Add '.' at the end
dataset['Robo_response'] = dataset['Robo_response'] + delimiter

# Specify the file name
file_name = 'testing.txt'

# Check if the file already exists
if os.path.isfile(file_name):
    try:
        # remove the existing file
        os.remove(file_name)
    except Exception as e:
        print(f"Error deleting the existing file: {e}")

# Write the DataFrame to a text file with .txt extension
dataset.to_csv(file_name, sep=':', index=False, header=False)  # Specify .txt extension

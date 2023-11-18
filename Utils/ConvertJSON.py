import pandas as pd
import json

# File path to your Excel file
excel_file_path = ''

df = pd.read_excel('C:\\Users\\admin\\Downloads\\tweet_information.xlsx')
df.to_json('new_file2.json', orient='records') # excel to json
# read json and then append details to it
with open('new_file2.json', 'r') as json_file: 
    a = {}
    data = json.load(json_file)
    a['details'] = data
# write new json with details in it
with open("new_file2.json", "w") as jsonFile:
    json.dump(a, jsonFile)
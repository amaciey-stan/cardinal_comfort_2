import pandas as pd

import re

from programs.data_cleaning.data_cleaning import box_data_cleaning

trends = pd.read_csv('../data/HWSysTrends11_5to11_12.csv')

# creates a list of building names based on regex patterns from the "Name Path Reference" column in the csv file
reg_list = [re.findall(r"(?<=\.)(B.*?)(?=\.)", i)[0] for i in trends['Name Path Reference']]

# adds the reg_list to the initial DataFrame as "Building"
trends['Building'] = reg_list

# Creates list of each Building name
buildings = pd.unique(trends['Building'])
cleaned_df = pd.DataFrame()

for i in buildings:
    # Creates two DataFrames with the same building name from the different csv files
    data = trends[trends['Building'] == i]

    data = box_data_cleaning(data)

    data['Building'] = i

    cleaned_df = cleaned_df.append(data)

cleaned_df.to_csv('weekly_cleaned_data.csv')

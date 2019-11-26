import pandas as pd

import os

from programs.data_cleaning.data_cleaning import box_data_cleaning

from programs.set_points_function.new_set_points import new_set_points, min_and_max

# Imports file of building names, groupings, meters, and csv filenames
groupings = pd.read_csv('../data/BuildingGroupings.csv')

groups = []
points = []
set_points_df = pd.DataFrame()

for root, dirs, files in os.walk("../data/last_year"):
    for filename in files:
        # reads and cleans data for each file
        data = pd.read_csv('../data/last_year/' + str(filename))
        data = box_data_cleaning(data)
        data['Filename'] = str(filename)
        data = data[data['Year'] == 2018]
        # calculates new set points
        new_set_points(data)

        # reduces the dataframe to only relevant columns
        data = data[['Week', 'Date', 'New Points Weekly', 'New Points Daily', 'Water Set Point', 'Outside Temp',
                     'Filename']]

        # concatenates all dataframes into one
        set_points_df = set_points_df.append(data)

        # adds group number and set point to each list respectively
        """groups.append(groupings[groupings['Csv Filenames'] == str(filename)]['Group Number'].values[0])
        points.append(min_and_max(data, 47))

# creates DataFrame of groups and set points to make copying into google easier
d = {'Groups': groups, 'Points': points}
full_points = pd.DataFrame(data=d)"""

# print(full_points)
set_points_df.to_csv('set_points.csv')

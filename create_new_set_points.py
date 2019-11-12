import pandas as pd

import matplotlib.pyplot as plt

import os

from programs.data_cleaning.data_cleaning import box_data_cleaning

from programs.set_points_function.new_set_points import new_set_points, energy_savings, min_and_max

groupings = pd.read_csv('../data/BuildingGroupings.csv')

groups = []
points = []

for root, dirs, files in os.walk("../data/last_year"):
    for filename in files:
        data = pd.read_csv('../data/last_year/' + str(filename))
        data = box_data_cleaning((data))
        new_set_points(data)
        # Fix the next line to return only the value of the group number
        groups.append(groupings[groupings['Csv Filenames'] == str(filename)]['Group Number'].values[0])
        points.append(min_and_max(data, 47))

d = {'Groups': groups, 'Points': points}

full_points = pd.DataFrame(data=d)

print(full_points)

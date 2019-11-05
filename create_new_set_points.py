import pandas as pd

import matplotlib.pyplot as plt

import os

from programs.data_cleaning.data_cleaning import box_data_cleaning

from programs.set_points_function.new_set_points import new_set_points, energy_savings, min_and_max

groupings = pd.read_csv('../data/BuildingGroupings.csv')

for root, dirs, files in os.walk("../data"):
    for filename in files:
        data = pd.read_csv('../data/' + str(filename))
        data = box_data_cleaning((data))
        new_set_points(data)
        print(groupings[groupings['Csv Filenames'] == str(filename)].iloc[:, 0])
        min_and_max(data, 46)

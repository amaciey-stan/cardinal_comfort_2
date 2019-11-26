import pandas as pd

from programs.data_cleaning.data_cleaning import box_data_cleaning

import numpy as np

from programs.set_points_function.new_set_points import new_set_points_2
import mysql.connector

"""db = mysql.connect(
    host = "localhost:38182	",
    user = "drdecardinalco",
    passwd = "Stanford1885"
)

print(db)"""

test_data = pd.read_csv('../data/last_year/B05_520Jerry.csv')

test_data = box_data_cleaning(test_data)

test_data['Filename'] = 'Jerry'

#print(test_data.groupby(['Filename', 'Week']).agg(min).index.values)

#print(np.unique(test_data['Week']))

mins_and_maxes = new_set_points_2(test_data)

variances = test_data.groupby(['Filename', 'Week']).agg(np.var)['Water Set Point']

# mins_and_maxes.loc[:'Variances'] = variances

print(variances)

# print(mins_and_maxes[mins_and_maxes['Week'] == 46])

"""test_data = test_data[['Date', 'Water Set Point', 'New Points Weekly', 'New Points Daily', 'Outside Temp', 'Week']]

test_data = test_data[test_data['Week'].isin([3,4,5,6,39,40,41,42,43,44,45,46,47,48])]

test_data['Ratio'] = test_data['New Points Weekly'] / test_data['Water Set Point']

print(test_data.groupby('Week').agg(min)['Ratio'])"""

#test_data.to_csv('../data/Jerry.csv')

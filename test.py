import pandas as pd

from programs.data_cleaning.data_cleaning import box_data_cleaning

import mysql.connector

db = mysql.connect(
    host = "localhost:38182	",
    user = "drdecardinalco",
    passwd = "Stanford1885"
)

print(db)

test_data = pd.read_csv('../data/B05_520Jerry.csv')

test_data = box_data_cleaning(test_data)

test_data['Building Name'] = 'Jerry'

print(test_data.head())

#test_data.to_csv('../data/Jerry.csv')
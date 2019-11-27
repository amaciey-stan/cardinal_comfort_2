import pandas as pd

import os

from zipfile import ZipFile

awair_df = pd.DataFrame()

file_name = "C:/Users/amaciey/PycharmProjects/cardinal_comfort/data/data.zip"

with ZipFile(file_name, 'r') as zip:
    for i in zip.namelist():
        # adds the building name to each individual csv file
        zip.extract(i)
        data = pd.read_csv(i)
        data['Building'] = str(i)

        # concatenates all dataframes into one
        awair_df = awair_df.append(data)

        os.remove(i)

awair_df = awair_df.merge(pd.read_csv('AWAIR_and_metasys.csv'), left_on='Building', right_on='AWAIR Name', how='inner')

awair_df.drop(columns=['Building'], inplace=True)

print(awair_df)

# awair_df.to_csv('weekly_awair.csv')

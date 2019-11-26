import pandas as pd

awair = pd.read_csv('AWAIR/mirrielees_AWAIR.csv')

awair.loc[:, 'temp (F)'] = awair.iloc[:, 1] * (9/5) + 32

awair.iloc[:, 0] = pd.to_datetime(awair.iloc[:, 0])

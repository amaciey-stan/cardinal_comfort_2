import pandas as pd

from AWAIR.AWAIR_data_cleaning import awair_df

from weekly_metasys_data_cleaning import cleaned_df

full_df = pd.merge(awair_df, cleaned_df, how='inner', left_on=['timestamp(America/Los_Angeles)', 'Metasys Name'],
                   right_on=['Date', 'Building'])

print(full_df.head())

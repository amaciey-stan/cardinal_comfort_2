import numpy as np

import pandas as pd


def setdiff_sorted(array1, array2, assume_unique=False):
    # Compares two series and returns the values from array 1 not found n array 2
    ans = np.setdiff1d(array1, array2, assume_unique).tolist()
    if assume_unique:
        return sorted(ans)
    return ans


def new_set_points(this_week, data):
    # Cleans google sheet data and creates new set point/weather combinations
    min_low = 110  # absolute lowest low set point
    min_high = 125  # absolute lowest high set point
    max_low = 130  # absolute highest low set point
    max_high = 140  # absolute highest high set point

    # creating dictionaries that reference the above points but adjust them for certain buildings based on AWAIR data
    low_set_points_dictionary = {'B1': min_low,
                                 'B2': (min_low + 7),
                                 'B3': (min_low + 7),
                                 'B4': (min_low + 5),
                                 'B5': min_low,
                                 'B6': min_low,
                                 'B7': min_low,
                                 'B8': (min_low + 5),
                                 'B9': min_low,
                                 'B10': min_low,
                                 'B11': min_low}

    high_set_points_dictionary = {'B1': min_high,
                                  'B2': (min_high + 7),
                                  'B3': (min_high + 7),
                                  'B4': (min_high + 5),
                                  'B5': min_high,
                                  'B6': min_high,
                                  'B7': min_high,
                                  'B8': (min_high + 5),
                                  'B9': min_high,
                                  'B10': min_high,
                                  'B11': min_high}

    potential_lows = np.arange(min_low, max_low)  # range of all acceptable low points
    potential_highs = np.arange(min_high, max_high)  # range of all acceptable high points

    set_points_columns = list(data.drop(['Date', 'Day of Week', 'Outside Temperature (Forecast)',
                                        'Observed Temperature', 'Maintenance Tech'], axis=1).columns)

    # Calculates moving average of low temperatures and adds a new column
    daily_low_averages = [np.mean(data.loc[i-3:i-1, 'Observed Temperature']) for i in data
                          .index.values]
    daily_low_averages[0] = 55
    data.loc[:, 'Moving Average Low'] = daily_low_averages

    upcoming_low_averages = [np.mean(this_week.loc[i - 3:i - 1, 'Outside Temperature (Forecast)']) for i in this_week
                             .index.values]
    upcoming_low_averages[0] = 55
    this_week.loc[:, 'Moving Average Low'] = upcoming_low_averages

    # New DataFrame for untried set points
    new_points = pd.DataFrame(columns=set_points_columns)

    # creates DataFrame of previous days with the same temperatures and previous averages as the coming week
    for i in this_week.index.values:
        low = this_week.loc[i, 'Outside Temperature (Forecast)']
        average = this_week.loc[i, 'Moving Average Low']
        observed_temperatures = data[(data['Observed Temperature'] == low) &
                                     (data['Moving Average Low'] == average)]

        day_points = []
        for j in set_points_columns:
            previous_set_points = observed_temperatures.loc[:, j]
            previous_highs = [i.split('/')[1] for i in previous_set_points]
            untried_highs = setdiff_sorted(potential_highs, previous_highs, assume_unique=True)
            best_point = untried_highs[0]
            day_points.append(str(min_low) + '/' + str(best_point))

        new_points = new_points.append(pd.Series(day_points, index=new_points.columns), ignore_index=True)

    return new_points

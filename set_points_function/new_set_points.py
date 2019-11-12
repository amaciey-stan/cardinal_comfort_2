import numpy as np



def new_set_points(data):
    # Creates a list of the new set points based weekly variances
    new_points_weekly = []

    # Calculates the weekly variance in water set points from last year
    variances_weekly = data.groupby('Week').agg(np.var)['Water Set Point']

    for i in variances_weekly.index.values:
        weekly = data[data['Week'] == i].reset_index()
        low = min(weekly['Water Set Point'])
        high = max(weekly['Water Set Point'])

        if variances_weekly[i] > 40:
            for i in weekly['Outside Temp']:
                if i > 56:
                    new_points_weekly.append(low * 0.95)
                else:
                    new_points_weekly.append(high * 0.9)

        elif 10 < variances_weekly[i] < 40:
            for i in weekly['Outside Temp']:
                if i > 56:
                    new_points_weekly.append(low * 0.98)
                else:
                    new_points_weekly.append(high * 0.9)

        else:
            for i in weekly['Outside Temp']:
                if i > 56:
                    new_points_weekly.append(low * 0.95)
                else:
                    new_points_weekly.append(high * 0.95)

    data.loc[:, 'New Points Weekly'] = new_points_weekly[::-1]

    # Creates a list of the new set points based on daily variances
    new_points_daily = []

    # Calculates the daily variance in water set points from last year
    variances_daily = data.groupby('Day').agg(np.var)['Water Set Point']

    for i in variances_daily.index.values:
        daily = data[data['Day'] == i].reset_index()
        low = min(daily['Water Set Point'])
        high = max(daily['Water Set Point'])

        if variances_daily[i] > 40:
            for i in daily['Outside Temp']:
                if i > 56:
                    new_points_daily.append(low)
                else:
                    new_points_daily.append(high * 0.98)

        elif 20 < variances_daily[i] < 40:
            for i in daily['Outside Temp']:
                if i > 56:
                    new_points_daily.append(low * 0.95)
                else:
                    new_points_daily.append(high * 0.98)

        else:
            for i in daily['Outside Temp']:
                if i > 56:
                    new_points_daily.append(low)
                else:
                    new_points_daily.append(high * 0.99)

    data.loc[:, 'New Points Daily'] = new_points_daily[::-1]


def energy_savings(data):
# Not finished. Will require an update when the model is completed
    print('Energy Savings: ' + str(sum(-1740.78 + (47.4439 * data['New Points Weekly'])) /
                                   sum(-1740.78 + (47.4439 * data['Water Set Point']))))

def min_and_max(data, week):
# prints the low and high set points separated by a slash
    return str(round(min(data[data['Week'] == week]['New Points Weekly']))) + '/' + str(round(max(data[data['Week'] == week]['New Points Weekly'])))

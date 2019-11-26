import pandas as pd
import datetime as dt


# Ensures that the data in question fall within the time frame that heat is usually turned on
def heating_season(data, start, end):
    return data[(data['Date'] >= (str(start) + '-10-01')) & (data['Date'] <= (str(end) + '-06-15'))]


# Ensures that the data in question fall within the shoulder season at the beginning and end of heating season
def shoulder_season(data, start, end):
    return data[(data['Date'] >= (str(start) + '-10-29')) & (data['Date'] <= (str(end) + '-12-15'))]


# Changes string values to numeric values so they can be analysed (strips 'deg F' off the ends)
def temperature_cleaning(data):
    cleaned = []
    for i in data:
        if type(i) == str:
            cleaned.append(float(i.split(' ', 1)[0]))
        else:
            cleaned.append(i)
    return cleaned


def box_data_cleaning(data):
    # creates DataFrame of outside Temp values and dates
    outside_temp = data[data['Object Name'] == 'OA-T.Trend - Present Value (Trend1)']
    oa_dates = pd.to_datetime(outside_temp['Date / Time'])
    outside_temp = temperature_cleaning(outside_temp['Object Value'])
    oa_data = pd.DataFrame(data={'Date': oa_dates, 'Outside Temp': outside_temp})

    # DataFrame of Set Point Values
    water_set = temperature_cleaning(data[data['Object Name'] == 'LTHWAFT-SP.Trend - Present Value (Trend1)']
                                     ['Object Value'])

    water_set_dates = pd.to_datetime(data[data['Object Name'] == 'LTHWAFT-SP.Trend - Present Value (Trend1)']
                                     ['Date / Time'])

    water_set_data = pd.DataFrame(data={'Date': water_set_dates, 'Water Set Point': water_set})

    # DataFrame of Supply Temp Values
    water_supply = temperature_cleaning(data[data['Object Name'] == 'HHWS-T.Trend - Present Value (Trend1)']
                                        ['Object Value'])

    water_supply_dates = pd.to_datetime(data[data['Object Name'] == 'HHWS-T.Trend - Present Value (Trend1)']
                                        ['Date / Time'])
    # DataFrame of Return Temp Values
    water_supply_data = pd.DataFrame(data={'Date': water_supply_dates, 'Water Supply Temp': water_supply})

    water_return = temperature_cleaning(data[data['Object Name'] == 'HHWR-T.Trend - Present Value (Trend1)']
                                        ['Object Value'])

    water_return_dates = pd.to_datetime(data[data['Object Name'] == 'HHWR-T.Trend - Present Value (Trend1)']
                                        ['Date / Time'])

    water_return_data = pd.DataFrame(data={'Date': water_return_dates, 'Water Return Temp': water_return})

    # Merging all four DataFrames into one based on Date columns
    data_full = water_set_data.merge(oa_data, on='Date', how='inner')
    data_full = data_full.merge(water_supply_data, on='Date', how='inner')
    data_full = data_full.merge(water_return_data, on='Date', how='inner')

    """Creating New Columns for day of year, week of year, and changing the date column to merge on 
    previous year's data"""
    data_full.loc[:, 'Week'] = data_full['Date'].dt.week
    data_full.loc[:, 'Day'] = data_full['Date'].dt.dayofyear
    data_full.loc[:, 'Year'] = data_full['Date'].dt.year
    data_full.loc[:, 'Date'] = data_full['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    return data_full

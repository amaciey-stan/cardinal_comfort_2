import pandas as pd

def heating_season(data, start, end):
    return data[(data['Date'] >= (str(start) + '-10-01')) & (data['Date'] <= (str(end) + '-06-15'))]


def shoulder_season(data, start, end):
    return data[(data['Date'] >= (str(start) + '-10-29')) & (data['Date'] <= (str(end) + '-12-15'))]


def temperature_cleaning(data):
    cleaned = []
    for i in data:
        if type(i) == str:
            cleaned.append(float(i.split(' ', 1)[0]))
        else:
            cleaned.append(i)
    return cleaned



"""Cleans data and creates a new dataframe for each csv file in the Box folder. Make sure they include the 
'LTHWAFT - SP' value"""


def box_data_cleaning(data, shoulder=False):
    outside_temp = data[data['Object Name'] == 'OA-T.Trend - Present Value (Trend1)']
    oa_dates = pd.to_datetime(outside_temp['Date / Time'])
    outside_temp = temperature_cleaning(outside_temp['Object Value'])
    oa_data = pd.DataFrame(data={'Date':oa_dates, 'Outside Temp': outside_temp})

    water_set = temperature_cleaning(data[data['Object Name'] == 'LTHWAFT-SP.Trend - Present Value (Trend1)']['Object Value'])
    water_set_dates = pd.to_datetime(data[data['Object Name'] == 'LTHWAFT-SP.Trend - Present Value (Trend1)']['Date / Time'])
    water_set_data = pd.DataFrame(data={'Date': water_set_dates, 'Water Set Point': water_set})

    water_supply = temperature_cleaning(data[data['Object Name'] == 'HHWS-T.Trend - Present Value (Trend1)']['Object Value'])
    water_supply_dates = pd.to_datetime(data[data['Object Name'] == 'HHWS-T.Trend - Present Value (Trend1)']['Date / Time'])
    water_supply_data = pd.DataFrame(data={'Date': water_supply_dates, 'Water Supply Temp': water_supply})

    water_return = temperature_cleaning(data[data['Object Name'] == 'HHWR-T.Trend - Present Value (Trend1)']['Object Value'])
    water_return_dates = pd.to_datetime(data[data['Object Name'] == 'HHWR-T.Trend - Present Value (Trend1)']['Date / Time'])
    water_return_data = pd.DataFrame(data={'Date': water_return_dates, 'Water Return Temp': water_return})

    data_full = water_set_data.merge(oa_data, on='Date', how='inner')
    data_full = data_full.merge(water_supply_data, on='Date', how='inner')
    data_full = data_full.merge(water_return_data, on='Date', how='inner')
    data_full.loc[:, 'Week'] = data_full['Date'].dt.week
    data_full.loc[:, 'Day'] = data_full['Date'].dt.dayofyear
    return data_full
    #print(data_full.head())

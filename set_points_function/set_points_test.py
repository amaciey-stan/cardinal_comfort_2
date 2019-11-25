import pandas as pd
import numpy as np

from new_set_points import new_set_points

test_data = pd.read_csv('test_data.csv')

next_week_data = pd.read_csv('next_week_test_data.csv')

test_points = new_set_points(next_week_data, test_data)

print(test_points)

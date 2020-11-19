"""
Формирую таблицу для обработки в ODV
"""

import pandas as pd


path_file = 'C:/Users/Egor/Desktop/new_cutter/cutter/joined/1930_6_nst.csv'
df = pd.read_csv(path_file, delimiter=',')
df = df.rename(columns={
                        'long': 'Longitude',
                        'lat': 'Latitude',
                        'zz': 'Depth_in_situ',
                        'level': 'Level',
                        'temp': 'Temperature',
                        'sal': 'Salinity',
                        'oxig': 'Oxigen',
                        'Stations': 'Station'
                        })

name_of_cruise = 'Other_name'
name_of_type = 'Other_type'
hour, minute, second = 0, 0, 0
df['Cruise'] = name_of_cruise
df['Type'] = name_of_type
df['Hour'], df['Minute'], df['Second'] = hour, minute, second
printing_df = df[['Cruise', 'Station', 'Type', 'Latitude', 'Longitude', 'Level', 'Year', 'Month', 'Day', 'Hour',
                  'Minute', 'Second', 'Temperature', 'Salinity', 'Oxigen']]

printing_df.to_csv('C:/Users/Egor/Desktop/new_cutter/cutter/joined/Oxig_to_ODV.csv', index=False)

print('OK')

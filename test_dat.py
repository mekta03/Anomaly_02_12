import pandas as pd


path_dir = '/home/lenovo/test_anomaly_new/'
name_dir_dat = 'dat_files/'
name_stations = 'Станции.csv'

parameter = 'oxig'

lst_levels = [0, 20, 50, 100, 200, 500]

lst_month = ['september', 'october']

# df_for_woa = pd.DataFrame()
# num = True
# for month in lst_month:
#     for lvl in lst_levels:
    
#         file = f'{path_dir}{name_dir_dat}woa_18_{month}_{lvl}m.dat'
#         name_of_clolumn = f'WOA_{month[:3]}_{lvl}m'

#         columns = ['long', 'lat', name_of_clolumn]
#         dff = pd.read_csv(file, sep=' ', engine='python', names=columns)
#         dff = dff.copy()
#         dff = dff.loc[dff[name_of_clolumn] < 100].round(3)
        
#         if num == True:
#             df_for_woa = pd.concat([df_for_woa, dff], axis=1)
#             num = False
#         else:
#             df_for_woa = pd.merge(df_for_woa, dff, on=['long', 'lat'])
#         print(month, lvl)

# df_for_woa = df_for_woa.rename(columns={'long':'Longitude', 'lat':'Latitude'})

# ===================================================================
df_nst = pd.read_csv(f'{path_dir}{name_stations}', sep=',')

df_nst['Date'] = pd.to_datetime(df_nst['Date'],format="%d.%m.%Y")
df_nst['Time'] = pd.to_datetime(df_nst['Time'])


df_nst['Year'] = df_nst['Date'].dt.year
df_nst['Month'] = df_nst['Date'].dt.month
df_nst['Day'] = df_nst['Date'].dt.day
df_nst['Hour'] = df_nst['Time'].dt.hour
df_nst['Minute'] = df_nst['Time'].dt.minute
df_nst['Second'] = df_nst['Time'].dt.second


df_nst = df_nst.drop(['Date', 'Time'], axis=1)
# print(df_nst)


# ========================================================================
# Попытка в одну колонку разные месяцы woa записать в зависимости от месяца станции
df_concated = pd.DataFrame()
dct_month = {'september':9,'october':10}

for name_month, num_month in dct_month.items():
    num = True
    df_for_woa = pd.DataFrame()

    df_nst_1 = df_nst.copy()

    df_nst_1 = df_nst_1.query('Month == @num_month')

    for lvl in lst_levels:
    
        file = f'{path_dir}{name_dir_dat}woa_18_{name_month}_{lvl}m.dat'
        name_of_clolumn = f'WOA_{lvl}m'

        columns = ['long', 'lat', name_of_clolumn]
        dff = pd.read_csv(file, sep=' ', engine='python', names=columns)
        dff = dff.copy()
        dff = dff.loc[dff[name_of_clolumn] < 100].round(3)
        
        if num == True:
            df_for_woa = pd.concat([df_for_woa, dff], axis=1)
            num = False
        else:
            df_for_woa = pd.merge(df_for_woa, dff, on=['long', 'lat'])
        print(name_month, lvl)
    
    print(df_for_woa)
    df_for_woa = df_for_woa.copy()
    df_for_woa = df_for_woa.rename(columns={'long':'Longitude', 'lat':'Latitude'})
    df_nst_1 = pd.merge(df_nst_1, df_for_woa, on=['Longitude','Latitude'])
    df_concated = pd.concat([df_concated, df_nst_1])
    

print(df_concated)
df_concated.to_csv(f'{path_dir}filtred_woa_new2.csv', sep=',', index=False)
# # =======================================
# df_new = pd.DataFrame()



# for month in dct_month:
#     num_month = dct_month[month]
#     df_nst = df_nst.copy()
#     df_nst = df_nst.query('Month == @month')


#     df_new = pd.merge(df_nst, df_for_woa, on=['Longitude', 'Latitude'])
# # df_new.to_csv(f'{path_dir}filtred_woa.csv', sep=',', index=False)



# dct_month = {'september':9,'october':10}
# df_concat = pd.DataFrame()
# df_orig = pd.read_csv(f'{path_dir}Safonov_17.09-17.10.csv')
# for month in lst_month:
#     num_month = dct_month[month]

#     df_month = df_orig.query('Month == @num_month')

#     for nst in sorted(df_month.Station.unique()):
#         df_one_station = df_month.query('Station == @nst')
        
        

#         for lvl in lst_levels:
#             df_lvl = df_one_station.query('level == @lvl')
#             df_lvl['WOA'] = df_new.query('Station == @nst')[[f'WOA_{month[:3]}_{lvl}m']]

#             df_concat = pd.concat([df_concat, df_lvl])


# print(df_concat.head())
# print()
# print(df_concat.describe())

# df_concat.to_csv(f'{path_dir}result.csv', index=False)
            







# woa_1 = 'Salinity_WOA_September'
# woa_2 = 'Salinity_WOA_October'

# df_original = pd.read_csv(path_original, sep=',')

# df_new = df_original.copy()
# grad = (df_new[woa_2] - df_new[woa_1])/30
# #print(grad)
# query1 = 'Day >= 15 and Month == 9'
# query2 = 'Day <= 15 and Month == 10'

# df_query_1 = df_new.query(query1)
# df_query_2 = df_new.query(query2)

# mean_for_date_1 = df_query_1[woa_1] + ((df_query_1['Day'] - 15) * grad)
# mean_for_date_2 = df_query_2[woa_2] + ((df_query_2['Day'] - 15) * grad)
# print(mean_for_date_1)
# anomaly_1 = (df_query_1['Salinity'] - mean_for_date_1).dropna()
# anomaly_2 = (df_query_2['Salinity'] - mean_for_date_2).dropna()

# finished_df = pd.concat([anomaly_1, anomaly_2],ignore_index=True)

# df_new['Anomaly'] = finished_df
# df_new.to_csv('C:/Users/Egor/Desktop/test_anomaly/test_test/to_ODV_with__anomaly.csv', index=False)

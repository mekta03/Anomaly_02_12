import pandas as pd

# Путь к проинтерполированному в Surfer атласу WOA и отфильтрованному по станциям
path_woa_salinity_september = 'C:/Users/Egor/Desktop/test_anomaly/filtered_interpolated_woa18_salinity_september.csv'
path_woa_salinity_october = 'C:/Users/Egor/Desktop/test_anomaly/filtered_interpolated_woa18_salinity_october.csv'

# Путь к файлу с данными о станциях (координаты, дата, время)
path_coord = 'C:/Users/Egor/Desktop/test_anomaly/Станции.csv'

# Путь к файлу с данными о станциях (температура, соленость, прочее)
path_data = 'C:/Users/Egor/Desktop/test_anomaly/Safonov_17.09-17.10.csv'

# Путь куда будет записан итоговый csv, с его названием
path_result_ODV = 'C:/Users/Egor/Desktop/test_anomaly/to_ODV.csv'

num_of_horizonts = 6                        # Кол-во горизонтов
std_horizonts = [0, 20, 50, 100, 200, 500]  # Глубина горизонтов
num_of_stations = 50                        # Кол-во станций
num_nst_first = 9                           # Номер первой станции
num_nst_last = 59                           # Номер последней станции
name_of_cruise = 'Safonov_20'               # Название Cruise
type_ = 'Rinko_ASTD'                        # Тип

"""
Добавляет данные по солености с зонда
"""
data_salinity_original_df = pd.read_csv(path_data, delimiter=',', encoding='1251')
#print(data_salinity_original_df)


# TODO НУЖНО ЗАМЕНИТЬ У НЕСКОЛЬКИХ СТАНЦИЙ 500 ГОРИЗОНТ НА ПОСЛЕДНИЙ ГОРИЗОНТ

#print(data_salinity_original_df.head(11))
# Разбить на отдельные файлы по станциям
# Если макс горизонт меньше 500, то либо None (добавить строку), либо подтянуть с макс глубины
# Объединить в один файл


def cutter_orig_file():
    """
    РАЗБИВАЕТ ОРИГИНАЛ ФАЙЛА НА НЕСКОЛЬКО ПО станциям
    """
    new_df = pd.read_csv('C:/Users/Egor/Desktop/test_anomaly/Safonov_17.09-17.10.csv', delimiter=',',encoding='1251')
    for nst in range(num_nst_first, num_nst_last):
        df = new_df.query('nst == @nst')
        if df['depth'].max() < 500:
            print(df.count())

            new_row = df.iloc[1]
            new_row['depth'] = 500
            new_row['temp'] = None
            new_row['sal'] = None
            new_row1 = pd.Series(new_row)
            df1 = df.append(new_row1,ignore_index=True)
            df1.to_csv('C:/Users/Egor/Desktop/test_anomaly/500m/cutted/'+f'{nst}.csv',index=False)
        else:
            df.to_csv('C:/Users/Egor/Desktop/test_anomaly/500m/cutted/'+f'{nst}.csv',index=False)


def joiner_clean_files():
    """
    ОБЪЕДИНЯЕТ ОЧИЩЕННЫЕ ФАЙЛЫ (ЗАМЕНЕНА ZZ, БЕЗ ПРОПУСКОВ, БЕЗ НУЛЕЙ В КИСЛОРОДЕ, БЕЗ ВЫБРОСОВ В T S)
    """

    # Сначала прописываешь в путь файл с первым годом (1930) а затем к нему уже плюсуешь остальные

    path_last = 'C:/Users/Egor/Desktop/test_anomaly/500m/cutted/joined/9.csv'
    df_last = pd.read_csv(path_last, header=0, delimiter=',')

    #new_orig_copy_df = pd.read_csv('C:/Users/Egor/Desktop/all_parameters_okhotskoe/new_orig_copy.csv', delimiter=',')

    new_df = pd.read_csv('C:/Users/Egor/Desktop/test_anomaly/Safonov_17.09-17.10.csv', delimiter=',', encoding='1251')
    for nst in range(10, num_nst_last):
        path_df_new = 'C:/Users/Egor/Desktop/test_anomaly/500m/cutted/' + f'{nst}.csv'
        df_new = pd.read_csv(path_df_new, delimiter=',')

        df_last = pd.concat([df_last, df_new])
        df_last.to_csv('C:/Users/Egor/Desktop/test_anomaly/500m/cutted/joined/9.csv', index=False)

    print('ok')



#cutter_orig_file()
joiner_clean_files()
        #df.to_csv('C:/Users/Egor/Desktop/test_anomaly/500m/cutted/'+f'{nst}.csv', index=False)
        #print(f'{nst}')








data_salinity_original_df_2 = data_salinity_original_df.query("depth == @std_horizonts")

salinity_original = data_salinity_original_df_2[['depth','sal']].reset_index(drop=True)
salinity_original = salinity_original.rename(columns={'depth':'Depth'})

df1 = pd.read_csv(path_result_ODV, delimiter=',')

#result_df = pd.merge(df1, salinity_original, on=['Depth'], how='inner')
#new_df = pd.concat([df1, salinity_original], axis=1, join='outer')
#print(df1['Salinity'])

"""
Добавляет данные по температуре с зонда
"""
data_temperature_original_df = pd.read_csv(path_data, delimiter=',', encoding='1251')
data_temperature_original_df_2 = data_temperature_original_df.query("depth == @std_horizonts")
temperature_original = data_temperature_original_df_2['temp'].reset_index(drop=True)
#print(temperature_original)



"""
Сначала образает файл атласа, потом берет проинтерполированный в Surfer атлас и фильтрует по нужным координатам
"""

import pandas as pd

min_latitude = 42
max_latitude = 62
min_longitude = 137.5
max_longitude = 165


def cutter(a, b, c, d):
    """

    Берет атлас с измененными заголовками и отбирает данные по заданным пределам координат,
    затем отсекает ненужные горизонты и сохраняет полученный файл атласа

    """
    #path_woa_original = 'C:/Users/Egor/Desktop/Anomal_13/woa_originals/woa13_salinity_october_.csv'
    #TEST
    for i in range(10,13):
        path_woa_original = 'C:/Users/Egor/Desktop/woa_for_oxygen/temp/original/woa18_A5B7_t'+f'{i}mn04.csv'
        path_result_original = 'C:/Users/Egor/Desktop/woa_for_oxygen/temp/cutted/woa18_'+f'{i}_cutted.csv'

        woa_df = pd.read_csv(path_woa_original, header = 1, delimiter=',')

        #list_of_columns = ['LATITUDE', 'LONGITUDE', '0', '20', '50', '100', '200', '500']
        new_woa_df = woa_df.rename(columns = {"#COMMA SEPARATED LATITUDE":'LATITUDE',' LONGITUDE':'LONGITUDE',
                                          ' AND VALUES AT DEPTHS (M):0':0})
        new_woa_df = new_woa_df.query("((LATITUDE >= @a) & (LATITUDE <= @b)) & ((LONGITUDE >= @c) & (LONGITUDE <= @d))")
        #new_woa_1_df = new_woa_df[list_of_columns]
        new_woa_df.to_csv(path_result_original, index=False)

        print('OKEY')

        # new_coord_station_df = coord_station_df.query("Depth == 0")


def filtration():
    """

    Берет атлас, в котором данные были проинтерполированы с помощью Surfer и файл с координатами станций,
    и отбирает данные в атласе по координатам станций,
    затем записывает результат в отдельный файл.

    """

    # Load files of WOA and station`s coordinates
    woa_df_october = pd.read_csv(path_woa_october, delimiter=';')
    woa_df_september = pd.read_csv(path_woa_september, delimiter=',')
    coord_df = pd.read_csv(path_coord, delimiter=',')

    # Merge files by only common coordinates and write result to new file
    result_september_df = pd.merge(coord_df, woa_df_september, on=['Latitude', 'Longitude'], how='inner')
    drop_df_sep = result_september_df.copy()
    new_drop_df_sep = drop_df_sep.drop(['Date', 'Time'], axis=1)
    new_drop_df_sep.to_csv(path_result_september)

    result_october_df = pd.merge(coord_df, woa_df_october, on=['Latitude', 'Longitude'], how='inner')
    drop_df_oct = result_october_df.copy()
    new_drop_df_oct = drop_df_oct.drop(['Date', 'Time'], axis=1)
    new_drop_df_oct.to_csv(path_result_october)

    """
    Фильтрую станции по октябрю
    

    #coord_october_df = [i.split('.') for i in coord_df['Date']]  # Разбивает дату 18.09.2020 по (.) на отд. части
    #new_coord_october_df = pd.DataFrame([i for i in coord_october_df]) #Добавляет это все датафрейм
    new_coord_october_df = new_coord_october_df.rename(columns={0: 'Day', 1: 'Month', 2: 'Year'}) # Переименовывает столбцы
    new_coord_october_df['Station'] = coord_df['Station']
    month_oct = '10'
    new_coord_october_df_2 = new_coord_october_df.query("Month == @month_oct")
    result_coord_october_df = pd.merge(new_coord_october_df_2, coord_df, on=['Station'], how='inner')
    #print(result_coord_october_df)
  
        Фильтрую станции по сентябрю
    
    coord_september_df = [i.split('.') for i in coord_df['Date']]  # Разбивает дату 18.09.2020 по (.) на отд. части
    new_coord_september_df = pd.DataFrame([i for i in coord_september_df])  # Добавляет это все датафрейм
    new_coord_september_df = new_coord_september_df.rename(columns={0: 'Day', 1: 'Month', 2: 'Year'})  # Переименовывает столбцы
    new_coord_september_df['Station'] = coord_df['Station']
    month_sep = '09'
    new_coord_september_df_2 = new_coord_september_df.query("Month == @month_sep")
    result_coord_september_df = pd.merge(new_coord_september_df_2, coord_df, on=['Station'], how='inner')
    #print(result_coord_september_df)
   
   
    new_df_all_season = pd.concat([result_september_df.iloc[:, 3:], result_october_df.iloc[:, 3:]])
    print(new_df_all_season)
    finished_new_df_all_season = new_df_all_season[['Station', 'Latitude', 'Longitude', 'Salinity_0m','Salinity_20m',
                                                       'Salinity_50m', 'Salinity_100m','Salinity_200m','Salinity_500m']]

    print(finished_new_df_all_season)
    finished_new_df_all_season.to_csv(path_common_result, index=False)

    print('OKEY')
    """

"""
Записываешь абсолютный (полный) путь к файлам (обратный слеш (косая черта) меняешь на обычный слеш)
"""
# Paths and names of work`s files
path_woa = 'C:/Users/Egor/Desktop/test_anomaly/interpolated_woa18_salinity_october.csv'
path_woa_october = 'C:/Users/Egor/Desktop/test_anomaly/interpolated_woa18_salinity_october.csv'
path_woa_september = 'C:/Users/Egor/Desktop/test_anomaly/interpolated_woa18_salinity_september.csv'
path_result_september = 'C:/Users/Egor/Desktop/test_anomaly/filtered_interpolated_woa18_salinity_september.csv'
path_result_october = 'C:/Users/Egor/Desktop/test_anomaly/filtered_interpolated_woa18_salinity_october.csv'
path_coord = 'C:/Users/Egor/Desktop/test_anomaly/Станции.csv'


if __name__ == '__main__':
    cutter(min_latitude, max_latitude, min_longitude, max_longitude)
    #filtration()
    #mover()
    #transponir()


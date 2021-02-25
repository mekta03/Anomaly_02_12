"""
Берет готовый файл с данными, который уже можно использовать для Surfer, и форматирует его для работы с ODV

"""
import pandas as pd


# Путь к проинтерполированному в Surfer атласу WOA и отфильтрованному по станциям
path_woa_salinity_september = 'C:/Users/Egor/Desktop/test_anomaly/filtered_interpolated_woa18_salinity_september.csv'
path_woa_salinity_october = 'C:/Users/Egor/Desktop/test_anomaly/filtered_interpolated_woa18_salinity_october.csv'

# Путь к файлу с данными о станциях (координаты, дата, время)
path_coord = 'C:/Users/Egor/Desktop/test_anomaly/Станции.csv'

# Путь к файлу с данными о станциях (температура, соленость, прочее)
path_data = 'C:/Users/Egor/Desktop/test_anomaly/Safonov_17.09-17.10_(NEW).csv'

# Путь куда будет записан итоговый csv, с его названием
path_result_ODV = 'C:/Users/Egor/Desktop/test_anomaly/to_ODV.csv'

num_of_horizonts = 6                        # Кол-во горизонтов
std_horizonts = [0, 20, 50, 100, 200, 500]  # Глубина горизонтов
num_of_stations = 50                        # Кол-во станций
num_nst_first = 9                           # Номер первой станции
num_nst_last = 59                           # Номер последней станции
name_of_cruise = 'Safonov_20'               # Название Cruise
type_ = 'Rinko_ASTD'                        # Тип


def maker_file_for_odv():
    """
    Форматирование таблицы для дальнейшего использование в ODV
    """
    # Создает пустой общий датафрейм
    result_df = pd.DataFrame(index=[i for i in range(num_of_stations*num_of_horizonts)])

    # Загружает атлас WOA salinity, проинтерполированный в Surfer
    woa_salinity_september_df = pd.read_csv(path_woa_salinity_september, delimiter=',')
    woa_salinity_october_df = pd.read_csv(path_woa_salinity_october, delimiter=',')
    """
    
    ДОБАВИТЬ АТЛАС С ТЕМПЕРАТУРОЙ И ВЫГРУЗИТЬ ИЗ НЕГО ЗНАЧЕНИЯ ТЕМПЕРАТУРЫ И ДОБАВИТЬ В НОВЫЙ ДАТАФРЕЙМ
    
    
    """
    # Переименовывает столбцы
    new_woa_salinity_september_df = woa_salinity_september_df.rename(columns={'Salinity_0m': 0,
                                                                              'Salinity_20m': 20,
                                                                              'Salinity_50m': 50,
                                                                              'Salinity_100m': 100,
                                                                              'Salinity_200m': 200,
                                                                              'Salinity_500m': 500})

    new_woa_salinity_october_df = woa_salinity_october_df.rename(columns={'Salinity_0m': 0,
                                                                          'Salinity_20m': 20,
                                                                          'Salinity_50m': 50,
                                                                          'Salinity_100m': 100,
                                                                          'Salinity_200m': 200,
                                                                          'Salinity_500m': 500})
    # Записывает данные в один столбец
    salinity_september_df = new_woa_salinity_september_df.iloc[:, 4:].stack().reset_index(drop=True)
    salinity_october_df = new_woa_salinity_october_df.iloc[:, 4:].stack().reset_index(drop=True)
    # Столбец с номерами станций, которые повторяются в зависимости от кол-ва горизонтов
    nst_df = pd.DataFrame([([i]*num_of_horizonts) for i in range(num_nst_first, num_nst_last+1)])
    nst_df = nst_df.stack().reset_index(drop=True)      # Переводит в один столбец

    # Столбец с горизонтами
    h_df = pd.DataFrame(std_horizonts * num_of_stations)

    # Столбец с координатами
    coord_df = pd.read_csv(path_coord, delimiter=',')   # Загружает файл с данными о станциях (коорд, дата, время)
    lat_df = pd.DataFrame([([i] * num_of_horizonts) for i in coord_df['Latitude']])     # Формирует столбец широт
    lat_df = lat_df.stack().reset_index(drop=True)                                      # Переводит в один столбец
    long_df = pd.DataFrame([([i] * num_of_horizonts) for i in coord_df['Longitude']])   # Формирует столбец долгот
    long_df = long_df.stack().reset_index(drop=True)                                    # Переводит в один столбец

    """
    НУЖНО ПРОВЕРЯТЬ ФОРМАТ ЗАПИСИ ДАТЫ И ВРЕМЕНИ
    """
    # Столбцы с датой (год, месяц, день)
    date_df = pd.read_csv(path_coord, delimiter=',')        # Загружает файл с данными о станциях (коорд, дата, время)
    new_date = [i.split('.') for i in date_df['Date']]     # Разбивает дату 18.09.2020 по (.) на отд. части
    new_date_df = pd.DataFrame([i for i in new_date])       # Записывает полученное данные о дате в датафрейм
    new_date_df = new_date_df.rename(columns={0: 'Day', 1: 'Month', 2: 'Year'})        # Переименовывает столбцы

    day_df = pd.DataFrame([([i] * num_of_horizonts) for i in new_date_df['Day']])      # Формирует столбец День
    day_df = day_df.stack().reset_index(drop=True)                                     # Переводит в один столбец
    month_df = pd.DataFrame([([i] * num_of_horizonts) for i in new_date_df['Month']])  # Формирует столбец Месяц
    month_df = month_df.stack().reset_index(drop=True)                                 # Переводит в один столбец
    year_df = pd.DataFrame([([i] * num_of_horizonts) for i in new_date_df['Year']])    # Формирует столбец Год
    year_df = year_df.stack().reset_index(drop=True)                                   # Переводит в один столбец

    # Столбцы со временем (часы, минуты, секунды)
    time_df = pd.read_csv(path_coord, delimiter=',')        # Загружает файл с данными о станциях (коорд, дата, время)
    new_time = [i.split(':') for i in time_df['Time']]      # Разбивает время 23:09:00 по (:) на отд. части
    new_time_df = pd.DataFrame([i for i in new_time])       # Записывает полученное данные о времени в датафрейм
    new_time_df = new_time_df.rename(columns={0: 'Hour', 1: 'Minute', 2: 'Second'})     # Переименовывает столбцы

    hour_df = pd.DataFrame([([i] * num_of_horizonts) for i in new_time_df['Hour']])        # Формирует столбец Часы
    hour_df = hour_df.stack().reset_index(drop=True)                                       # Переводит в один столбец
    minute_df = pd.DataFrame([([i] * num_of_horizonts) for i in new_time_df['Minute']])    # Формирует столбец Минуты
    minute_df = minute_df.stack().reset_index(drop=True)                                   # Переводит в один столбец
    second_df = pd.DataFrame([([i] * num_of_horizonts) for i in new_time_df['Second']])    # Формирует столбец Секунды
    second_df = second_df.stack().reset_index(drop=True)                                   # Переводит в один столбец


    """
    ТЕМПЕРАТУРА И СОЛЕНОСТЬ ЕСТЬ НЕ НА ВСЕХ ГОРИЗОНТАХ ПРОВЕРИТЬ
    """

    """
    Добавляет данные по солености с зонда
    """
    data_salinity_original_df = pd.read_csv(path_data, delimiter=',', encoding='1251')
    data_salinity_original_df_2 = data_salinity_original_df.query("depth == @std_horizonts")
    salinity_original = data_salinity_original_df_2['sal'].reset_index(drop=True)

    """
    Добавляет данные по температуре с зонда
    """
    data_temperature_original_df = pd.read_csv(path_data, delimiter=',', encoding='1251')
    data_temperature_original_df_2 = data_temperature_original_df.query("depth == @std_horizonts")
    temperature_original = data_temperature_original_df_2['temp'].reset_index(drop=True)


    # Добавляет сформированные столбцы с данными в созданный ранее общий датафрейм
    result_df['Cruise'] = name_of_cruise
    result_df['Station'] = nst_df
    result_df['Type'] = type_
    result_df['Depth'] = h_df
    result_df['Latitude'] = lat_df
    result_df['Longitude'] = long_df
    result_df['Year'] = year_df
    result_df['Month'] = month_df
    result_df['Day'] = day_df
    result_df['Hour'] = hour_df
    result_df['Minute'] = minute_df
    result_df['Second'] = second_df
    result_df['Salinity'] = salinity_original
    result_df['Temperature'] = temperature_original
    result_df['Salinity_WOA_September'] = salinity_september_df
    result_df['Salinity_WOA_October'] = salinity_october_df

    # Собирает столбцы в определённом порядке
    finished_df = result_df[['Cruise', 'Station', 'Type', 'Latitude', 'Longitude', 'Depth', 'Year',
                            'Month', 'Day', 'Hour', 'Minute', 'Second', 'Salinity','Temperature',
                             'Salinity_WOA_September', 'Salinity_WOA_October']]

    # Записывает полученную таблицу в csv файл
    finished_df.to_csv(path_result_ODV, index=False)
    print('Ok')


if __name__ == '__main__':
    maker_file_for_odv()


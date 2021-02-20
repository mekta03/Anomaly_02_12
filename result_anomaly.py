import pandas as pd

"""
=============================================
Производит расчет аномалий
=============================================

ЧТО НЕОБХОДИМО СДЕЛАТЬ:

- подготовить атласы (проинтерполировать - Surfer -> Kriging);
- создать папку, в которой будут:

    - папки с подготовленными атласами, в зависимости от исследуемых параметров;
      (например папка salinity, а в ней woa18_salinity_september.csv или woa18_salinity_9.csv....
      папка temperature, а в ней woa18_temperature_september.csv или woa18_temperature_9.csv..... и т.д.).
            
            Файлы атласов должны быть в формате csv, а названия:

                woa18_salinity_september.csv  или   woa18_salinity_9.csv

            Вместо salinity может быть temperature, dissolved_oxygen, nitrate, silicate, phospaht. 
            Название параметра ('salinity', 'temperature', и др.) должны быть одинаковы везде:
            - в таблице с исходными данными (в названии колонки);
            - в имени файла атласа (например 'woa18_salinity_september');

            Формат записи месяца может быть прописью или числом (1...12 без 0).
            Далее в программе нужно прописать какой формат используется "Пропись" или "Число".


    - файл с исходными данными, в котором указаны координаты, дата, номер станций и значения параметров. 
      Колонки должны быть строго в следующем формате, но порядок любой:
      Latitude, Longitude, Station, Year, Month, Day, level, salinity (или какой-то другой из параметров)


- прописать абсолютный (полный) путь к созданной рабочей папке,в которой будут:
    - папки с атласами; 
    - файл с исходными данными;
    (в эту же папку будет записан результат расчета.)

- указать название файла с исходными данными;
- указать название файла куда будет записан результат.


После произвести запуск программы
Расчет программы производится, пока не будет сообщение о завершении работы.


!!!!!!!! ВАЖНО !!!!!!!!
Для работы программы необходимо наличие в системе python и библиотеки pandas (установка требуется всего лишь один раз):
Установка python:

https://www.python.org/

Установка библиотеки pandas
 - выполнить в терминале следующие команды (которые со знаком $, но этот знак не прописывать):

    $ python install pip 
    
    (pip - это менеджер установки пакетов в python, нужен для установки pandas)
    если ошибка, то можно поробовать:

    $ python3 install pip
    
    затем:

    $ pip install pandas

    (если ошибка " Command 'pip' not found " попробовать следующую команду)
    
    $ pip3 install pandas

"""
# ================================================================================================================
# Начало выбора параметров

# Путь к рабочей папке, в которой будут файл с исходными данными, папки с атласами, и куда будет записан результат расчета
# (вписать путь к папке в ковычки)
path_dir = '/media/lenovo/D/Life/Работа/ТИНРО/Программы/Атласы (World Ocean Atlas)/test_anomaly/'
# path_dir = 'D:/Life/Работа/ТИНРО/Программы/Атласы (World Ocean Atlas)/test_anomaly/'

# Название файла csv с исходными данными (вписать название своего файла в ковычки)
name_df = 'Safonov_new_lvl.csv'

# Название файла csv, который будет создан с результатами расчета (отдельно создавать его не нужно)
# (вписать название своего файла в ковычки)
name_result = 'anomaly_result.csv'

# Параметры для которых будет произведён расчет аномалий (можно дописать в таком же формате через запятую)
# к примеру 'nitrate', 'dissolved_oxygen', 'silicate', 'phosphat'
lst_of_parameter = [
                    'salinity',
                    'temperature',
                    ]

# Список уровней, для которых будет расчет аномалий (можно изменить или дописать в таком же формате через запятую)
lst_levels = [0, 20, 50, 100, 200, 500]

# Вариант названия месяца в названии файла атласа, 
#   "Пропись" - "woa18_tempreture_september"
#   "Число"   - "woa18_tempreture_9"
# Прописать нужный вариант 
kind_name_of_month = "Число"


# Конец выбора параметров, далее необходимо произвести запуск программы.
# ================================================================================================================


def name_of_month(month:int) -> str:
    """
    Возвращает название месяца согласно номеру
    """
    dct_month = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'Jule', 8: 'August',
                 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

    return dct_month[month]


def month_for_atlas_by_day(month:int, day:int)->dict:
    """
    Определяет нужные месяца для атласов в зависимости от выбранного дня текущего месяца, создает словарь '01':'January'\n
    month - месяц 01..12 \n
    day - день месяца 01..31 \n
    """

    dct_month_atlas = {}
    for d in day:
        if d < 15:
            # Тогда нужен еще и атлас за ПРЕДЫДУЩИЙ месяц 
            num_month_atlas = (month-1 if month > 1 else 12)
        else:
            # Тогда нужен еще и атлас за СЛЕДУЮЩИЙ месяц 
            num_month_atlas = (month+1 if month < 12 else 1)
 
        name_month_atlas = name_of_month(num_month_atlas)
        dct_month_atlas[num_month_atlas] = name_month_atlas
        
    return dct_month_atlas


def make_dct_of_all_month_for_atlas(df)->dict:
    """
    Определяет все месяца для атласов для переданной таблицы данных \n
    """
    dct_of_month_for_atlas = {}

    lst_month_u = sorted(df['Month'].unique())

    for month in lst_month_u:

        if month == lst_month_u[0] or month == lst_month_u[-1]:
            df_1 = df.query('Month == @month')['Day']
            days =  [df_1.min(), df_1.max()]

            a = month_for_atlas_by_day(month, days)

            for k, v in a.items():
                dct_of_month_for_atlas[k] = v

            dct_of_month_for_atlas[month] = name_of_month(month)

        else:
            name_7 = name_of_month(month)
            dct_of_month_for_atlas[month] = name_7


    return dct_of_month_for_atlas


def make_woa_df(df):
    """
    Создает таблицу с данными из атласов
    """
    # Таблица с данными из нужных атласов
    woa_global = pd.DataFrame()

    dff = df.copy().query('level == 0')

    if kind_name_of_month == "Пропись":
        lst_name_of_month = dct_of_month_for_atlas.values()
    else:
        lst_name_of_month = dct_of_month_for_atlas.keys()
    
    for parameter in lst_of_parameter:
        for month in lst_name_of_month:

            # название файла атласа 
            name_woa = f'{path_dir}{parameter}/woa18_{parameter}_{month}.csv'

            woa_df_1 = pd.read_csv(name_woa, sep=',')

            # TODO имена для lat long
            # TODO Вывести список колонок в аргументы функции
            # TODO сделать необязательным колонку Station
            # TODO если нет Station изменить выбор диапазона колонок

            name_columns_woa = ['Latitude', 'Longitude', *lst_levels]
            woa_df_1 = woa_df_1[name_columns_woa]
            
            woa_df_1_new = pd.merge( dff[['Station', 'Latitude', 'Longitude']], woa_df_1,  on=['Latitude', 'Longitude'], how='inner')

            for lvl in name_columns_woa[2:]:

                woa_df_1_new = woa_df_1_new.rename(columns={lvl:f'WOA_{parameter}_{month}_{lvl}'})
            
            if woa_global.empty:
                woa_global = pd.concat([woa_global, woa_df_1_new])

            else:
                woa_global = pd.concat([woa_global, woa_df_1_new.iloc[:,3:]], axis=1)

    # woa_global.to_csv(f'{path_dir}WOA_ALL.csv', index=False)
   
    return woa_global


def make_df_for_define_anomaly(df, df_woa):
    """
    Создает таблицу с исходными данными и нужными данными из атласов для дальнейшего расчета аномалий\n
    df - таблица с исходными данными \n
    df_woa - таблица с данными из атласов \n
    """
    lst_month_u = sorted(df['Month'].unique())

    df_concat_all = pd.DataFrame()
    
    df_for_anomal = df.copy()

    for month in lst_month_u:

        df_mn = df_for_anomal.query('Month == @month')

        for day in df_mn['Day'].unique():
            df_day = df_mn.query('Day == @day')
            a = month_for_atlas_by_day(month, [day])
            
            # достаю значение из словаря
            if kind_name_of_month == "Пропись":
                mn_atlas_1 = dct_of_month_for_atlas[month]
                mn_atlas_2 = ''.join(a.values())
            else:
                mn_atlas_1 = month
                mn_atlas_2 = int(*a.keys())

            for lvl in df_day['level'].unique():
                df_lvl = df_day.query('level == @lvl')

                # TODO возможно стоит пробегаться не нст, а делать группировку по координатам и по группам
                for nst in df_lvl['Station'].unique():
                    df_nst = df_lvl.query('Station == @nst')
                    for parameter in lst_of_parameter:
                        name_woa_1 = f'WOA_{parameter}_{mn_atlas_1}_{lvl}'
                        name_woa_2 = f'WOA_{parameter}_{mn_atlas_2}_{lvl}'
                        
                        df_nst = df_nst.copy()
                        
                        df_nst[[f'WOA_{parameter}_1']] = [df_woa.query('Station == @nst')[name_woa_1]]
                        df_nst[[f'WOA_{parameter}_2']] = [df_woa.query('Station == @nst')[name_woa_2]]

                        
                    df_concat_all = pd.concat([df_concat_all, df_nst])

    df_concat_all = df_concat_all.sort_values(by=['Station', 'level'])

    return df_concat_all
    

def define_anomaly(df, parameter:str):
    """
    Производит расчет аномалий \n
    df - таблица, в которой уже присутствуют данные из необходимых атласов \n
    parameter - выбранный параметр, к примеру ...'Temperature','Salinity'... \n
    """
    print(f'Рассчитываю аномалии для {parameter.capitalize()}')
    # ! WOA_{parameter}_1 = Текущий месяц
    # ! WOA_{parameter}_2 = Следующий или предыдущий месяц, в зависимости от даты текущей станции
    df = df.copy()
    
    # На сколько изменяется значение в сутки
    grad = (df[f'WOA_{parameter}_2'] - df[f'WOA_{parameter}_1'])/30

    # Среднее значение для даты станции
    mean_for_date = df[f'WOA_{parameter}_1'] + ((df['Day'] - 15) * grad)

    # Разница между фактическим значеним и расчитанным средним значением
    anomaly = (df[parameter] - mean_for_date).dropna()

    df_anomaly = pd.DataFrame(data={f'anomaly_of_{parameter}': anomaly})

    return df_anomaly


# Путь к файлу с исходными данными
path_df = f'{path_dir}{name_df}'

# Путь к файлу с полученными результатами
path_for_result = f'{path_dir}{name_result}'


# Таблица с исходными данными
df = pd.read_csv(path_df, sep=',')

# Округляю координаты
df = df.copy()
df[['Longitude', 'Latitude']] = df[['Longitude', 'Latitude']].round(2)

# Фильтрует исходные данные по заданным горизонтам
df = df.query('level in @lst_levels')


# Перевод в строки уровни в цифрах
lst_levels = [str(i) for i in lst_levels]

# Словарь со всеми месяцами для выбора атласов
dct_of_month_for_atlas = make_dct_of_all_month_for_atlas(df)

# Таблица с данными из атласов
df_woa = make_woa_df(df)

# Таблица с исходными данными и данными из атласов для дальнейшего расчета аномалий
df_for_define_anomaly = make_df_for_define_anomaly(df, df_woa)

# Таблица с результатом
df_anomaly_all_parameter = pd.DataFrame()



# первая итерация для создания таблицы : исходные данные + данные атласов + аномалия для одного из параметров
# последующие итерации добавляют только расчитанные аномалии
print('=============================================================\n')

for parameter in lst_of_parameter:
    
    # Таблица с расчитанными аномалиями
    df_anomaly = define_anomaly(df_for_define_anomaly, parameter).round(2)

    # Удаляет столбцы с данными из атласов, которые нужны были для расчета аномалий (ПОКА не удаляет, надо убрать #)
    #df_for_define_anomaly = df_for_define_anomaly.drop([f'WOA_{parameter}_1', f'WOA_{parameter}_2'], axis=1)
    
    # Первая итерация (если в таблица пустая)
    if df_anomaly_all_parameter.empty:
        # Добавляю в пустую таблицу исходные данные + данные атласов + аномалия для одного из параметров
        df_for_define_anomaly = pd.concat([df_for_define_anomaly, df_anomaly], axis=1)
        df_anomaly_all_parameter= pd.concat([df_anomaly_all_parameter, df_for_define_anomaly])


    # Последующие итерации
    else:
        # В таблицу с (исходные данные, данные атласов, аномалия для одного из параметров) добавляю + аномалия для следующего из параметров
        df_anomaly_all_parameter= pd.concat([df_anomaly_all_parameter, df_anomaly], axis=1)
#     print(df_anomaly_all_parameter.query('level == 0'))
#     print(df_anomaly_all_parameter.query('level == 0')[[f'WOA_{parameter}_1', f'WOA_{parameter}_2',f'anomaly_of_{parameter}']].head())


print(df_anomaly_all_parameter)
# df_anomaly_all_parameter.to_csv(path_for_result, index=False)
print("Дело сделано!")


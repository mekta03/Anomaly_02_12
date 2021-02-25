"""
Производит линейную интерполяция в глубину
Переводит дату в UNIX формат
Разбивает исходный DataFrame на стд горизонты и дно
Записывает эти файлы в csv

"""
import pandas as pd

# Путь к папке проекта
# path_project = 'C:/Users/malyg/Desktop/kag_64/'
path_project = "D:/Life/Работа/ТИНРО/Текущие проекты/Kaganovsky_2020/kag_64/"
path_orig = f'{path_project}kag64_chem.csv'

df = pd.read_csv(path_orig, sep=',')
# Делает интерполяцию, True - делает, False - не делает (нужное вписать)
make_interpolation = True


# Границы уровней
dct_1 = {i: i + 9 for i in range(0, 31, 10)}
dct_2 = {i: i + 19 for i in range(30, 31)}
dct_3 = {i: i + 24 for i in range(50, 99, 25)}
dct_4 = {i: i + 49 for i in range(100, 251, 50)}
dct_5 = {i: i + 99 for i in range(300, 600, 100)}
dct_6 = {i: i + 99 for i in range(600, 1001, 200)}
# dct_7 = {i: i + 199 for i in range(1000, 1200, 200)}
dct_std_lvl = {**dct_1, **dct_2, **dct_3, **dct_4, **dct_5, **dct_6 }
std_lvl = [*dct_std_lvl.keys()]



def interpolation(df, col_for_inter:str, first_col:int, last_col= None):
    """
    Производит линейную интерполяцию \n
    col_for_inter - колонка для интерполяции (основа) \n
    first_col - начало диапазона колонок для интерполяции (результат) \n
    first_col - может быть списком из колонок, которые нужно проинтерполировать \n
    last_col - конец диапазона, если не указан, то до конца \n
    """
    df = df.copy()

    main_column = col_for_inter

    start_range = first_col
    
    if type(start_range) != list:
        end_range = last_col
        range_cols = df.columns[start_range:end_range]
    else:
        range_cols = df.columns[start_range]

    max_value = int(df[main_column].max())

    df_concat = pd.DataFrame()
    
    # Для того чтобы сначала записать данные в df а потом уже слияние производить
    flag = True
    for col in range_cols:
        df1 = df[[main_column, col]].copy()
        df_inter = pd.DataFrame(data={main_column: [i for i in range(0, max_value, 1)]},
                                index=[i for i in range(0, max_value, 1)])

        df_inter = pd.merge(df_inter, df1[[main_column, col]], how='outer', on=main_column)

        df_inter = df_inter.interpolate(limit_direction='backward', limit_area='inside')
        
        if flag:
            df_concat = pd.concat([df_concat, df_inter])
            flag = False
        else:
            df_concat = pd.merge(df_concat,df_inter, on=main_column)

    return df_concat
    

df_for_concat_all_lvl = pd.DataFrame()
df_for_concat_last_lvl = pd.DataFrame()
num_iter = 1
for nst in sorted(df['Station'].unique()):
    df_new = df.query('Station == @nst')

    num_cols = [*range(1,10), *range(11,20)]


    df_new = interpolation(df_new, 'level', num_cols)
    if df_new['Data_num'].max() - df_new['Data_num'].min() >= 1:
        print(df_new['Data_num'].describe())
    # Преобразовывает время в одну колонку datetime
    df_new['NewTime'] = pd.to_datetime(df_new[['day', 'month', 'year', 'hour', 'minute']],format="%d.%m.%Y.%h.%m")

    # Переводит из datetime в UNIX
    df_new['UnixTime'] = (df_new['NewTime'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

    df_new = df_new.drop('NewTime', axis=1)
    df_new = df_new.reset_index(drop=True)

    df_new = df_new.round(3)
    

    # Создает df c стд горизонтами
    df_new_std = df_new.query('level in @std_lvl')
    df_for_concat_all_lvl = pd.concat([df_for_concat_all_lvl, df_new_std])

    # Создает df c последним горизонтом
    max_lvl = df_new['level'].max()
    df_for_concat_last_lvl = pd.concat([df_for_concat_last_lvl, df_new.query('level == @max_lvl')])

    num_iter += 1
    print(len(df['Station'].unique()) - num_iter)

print(df_for_concat_all_lvl.columns)
print()
print(df_for_concat_all_lvl)

new_col_name = ['level', 'Station', 'day', 'month', 'year', 'hour', 'minute', 'Longitude', 'Latitude', 'Depth',
                'Data_num', 'UnixTime','Temperature', 'Salinity', 'O2', 'O2_%', 'Si', 'PO4', 'NO2', 'NO3', ]

df_for_concat_all_lvl = df_for_concat_all_lvl[new_col_name]

# Запись в один csv всех горизонтов  
df_for_concat_all_lvl.to_csv(f'{path_project}csv_new_2/csv/ALL_LVL.csv', index=False)

# Запись в отдельные csv отдельные горизонты  
for lvl in std_lvl:
    dff  = df_for_concat_all_lvl.query('level == @lvl')
    dff.to_csv(f'{path_project}csv_new_2/csv/{lvl}.csv', index=False)

# Запись в csv последний горизонт
df_for_concat_last_lvl = df_for_concat_last_lvl[new_col_name]
df_for_concat_last_lvl.to_csv(f'{path_project}csv_new_2/csv/last_lvl.csv', index=False)

"""
Производит расчет аномалий
"""
import pandas as pd
import re
import numpy as np


path_dir = '/home/lenovo/test_anomaly_new/'

name_dir_dat = 'dat_files/'
name_stations = 'Станции.csv'

lst_of_parameter = [
                    'salinity',
                    'temperature']

lst_levels = [0, 20, 50, 100, 200, 500]
lst_levels = [str(i) for i in lst_levels]
# lst_levels = ['0', '20']

def name_of_month(month):
    """
    Возвращает название месяца согласно номеру
    """
    dct_month = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'Jule', 8: 'August',
                 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

    return dct_month[month]


# path_dfff = '/media/lenovo/D/Life/Работа/ТИНРО/Программы/Атласы (World Ocean Atlas)/test_anomaly/Safonov_for_anomal.csv'
path_dfff = 'D:/Life/Работа/ТИНРО/Программы/Атласы (World Ocean Atlas)/test_anomaly/Safonov_for_anomal.csv'
dfff=pd.read_csv(path_dfff, sep=',')
dfff = dfff.copy()
dfff[['Longitude', 'Latitude']] = dfff[['Longitude', 'Latitude']].round(2)


def define_atlas_for_day(month, day):
    """
    Определяет нужные атласы, создает словарь '01':'January'
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


new_dct_atlas = {}
lst_month_u = sorted(dfff['Month'].unique())

# Определяю необходимые атласы
for month in lst_month_u:

    if month == lst_month_u[0] or month == lst_month_u[-1]:
        df_1 = dfff.query('Month == @month')['Day']
        days =  [df_1.min(), df_1.max()]

        a = define_atlas_for_day(month, days)

        for k, v in a.items():
            new_dct_atlas[k] = v

        new_dct_atlas[month] = name_of_month(month)

    else:
        name_7 = name_of_month(month)
        new_dct_atlas[month] = name_7


print(new_dct_atlas)

"""
	беру бд с загруженными атласами 
		атлас_месяц_лвл и атлас_МЕСЯЦ + - 1 _лвл
"""


#============================================
# ! ПОДГОТОВКА WOA DF
# TODO КАК то добавить возможность с параметром
woa_global = pd.DataFrame()
flag = True
# path_dir = r'D:/Life/Работа/ТИНРО/Программы/Атласы (World Ocean Atlas)/test_anomaly/'
# path_dir = '/home/lenovo/Документы/test_anomaly/temperature/dat/'
# path_dir = '/media/lenovo/D/Life/Работа/ТИНРО/Программы/Атласы (World Ocean Atlas)/test_anomaly/'
path_dir = 'D:/Life/Работа/ТИНРО/Программы/Атласы (World Ocean Atlas)/test_anomaly/'

for parameter in lst_of_parameter:
    for month in new_dct_atlas.values():

        # todo добавить путь к папке с woa и parameter

        name_woa_1 = f'{path_dir}{parameter}/dat/woa18_{parameter}_{month}.csv'

        woa_df_1 = pd.read_csv(name_woa_1, sep=',')

        # todo имена для lat long

        name_columns_woa = ['Latitude', 'Longitude', *lst_levels]
        woa_df_1 = woa_df_1[name_columns_woa]
        df_l  = dfff[['Latitude', 'Longitude']]
        woa_df_1_new = pd.merge( dfff[['Station', 'Latitude', 'Longitude']], woa_df_1,  on=['Latitude', 'Longitude'], how='inner')

        for lvl in name_columns_woa[2:]:

            woa_df_1_new = woa_df_1_new.rename(columns={lvl:f'WOA_{parameter}_{month}_{lvl}'})
        
        if flag:
            woa_global = pd.concat([woa_global, woa_df_1_new])
            flag=False
        else:
            woa_global = pd.concat([woa_global, woa_df_1_new.iloc[:,3:]], axis=1)

# !ВРОДЕ как до этого момента все правильно делает, нужно в ручную пересчитать аномалии
# woa_global.to_csv('/media/lenovo/D/Life/Работа/ТИНРО/Программы/Атласы (World Ocean Atlas)/test_anomaly/WOA_ALL.csv', index=False)

# ==========================================
# new_dct_atlas = {}
lst_month_u = sorted(dfff['Month'].unique())

df_concat_all = pd.DataFrame()
# path_for_anomal = '/media/lenovo/D/Life/Работа/ТИНРО/Программы/Атласы (World Ocean Atlas)/test_anomaly/Safonov_new_lvl.csv'
path_for_anomal = 'D:/Life/Работа/ТИНРО/Программы/Атласы (World Ocean Atlas)/test_anomaly/Safonov_new_lvl.csv'
df_for_anomal = pd.read_csv(path_for_anomal, sep=',')
# df_for_anomal = df_for_anomal.query('Station > 9')

for month in lst_month_u:

    df_mn = df_for_anomal.query('Month == @month')

    for day in df_mn['Day'].unique():
        df_day = df_mn.query('Day == @day')
        a = define_atlas_for_day(month, [day])
        
        # достаю значение из словаря
        mn_atlas_1 = new_dct_atlas[month]
        mn_atlas_2 = ''.join(a.values())
        

        for parameter in lst_of_parameter:
            for lvl in df_day['level'].unique():
                df_lvl = df_day.query('level == @lvl')
                for nst in df_lvl['Station'].unique():
                    df_nst = df_lvl.query('Station == @nst')
                    name_woa_1 = f'WOA_{parameter}_{mn_atlas_1}_{lvl}'
                    name_woa_2 = f'WOA_{parameter}_{mn_atlas_2}_{lvl}'
                    
                    df_nst = df_nst.copy()
                    
                    df_nst[[f'WOA_{parameter}_1']] = [woa_global.query('Station == @nst')[name_woa_1]]
                    # print(woa_global.query('Station == @nst')[name_woa_1])
                    # print(df_nst)
                    df_nst[[f'WOA_{parameter}_2']] = [woa_global.query('Station == @nst')[name_woa_2]]

                    # TODO Изменить расположение df_concat_all или метод сложения, т.к. скорее всего при множестве параметров будет ошибка

                    df_concat_all = pd.concat([df_concat_all, df_nst])

df_concat_all = df_concat_all.sort_values(by=['Station', 'level'])
# print(df_concat_all)

# ===================================================
def define_anomaly(df, parameter):
    # ! Расчет аномалий

    # ! woa_1 = ТЕкущий месяц
    # ! woa_2 = Следующий или предыдущий месяц
    df = df.copy()
    
    # На сколько изменяется значение в сутки
    grad = (df[f'WOA_{parameter}_2'] - df[f'WOA_{parameter}_1'])/30

    # Среднее значение для даты станции
    mean_for_date = df[f'WOA_{parameter}_1'] + ((df['Day'] - 15) * grad)

    # Разница между фактическим значеним и расчитанным средним значением
    anomaly = (df[parameter] - mean_for_date).dropna()
    # anomaly_2 = (df_query_2['Salinity'] - mean_for_date_2).dropna()

    # finished_df = pd.concat([anomaly_1, anomaly_2],ignore_index=True)
    return anomaly

    # df[f'Anomaly_{parameter}'] = anomaly_1

# ====================================================

df_anomaly_all_parameter = pd.DataFrame()

for parameter in lst_of_parameter:
    s_anomaly = define_anomaly(df_concat_all, parameter)
    df_anomaly = pd.DataFrame(data={f'anomaly_of_{parameter}':s_anomaly}).round(2)

    # df_concat_all = df_concat_all.drop([f'WOA_{parameter}_1', f'WOA_{parameter}_2'], axis=1)
    
    df_concat_all = pd.concat([df_concat_all, df_anomaly], axis=1)
    df_anomaly_all_parameter= pd.concat([df_anomaly_all_parameter, df_concat_all])
    print(df_anomaly_all_parameter.query('level == 0'))
    print(df_anomaly_all_parameter.query('level == 0')[[f'WOA_{parameter}_1', f'WOA_{parameter}_2',f'anomaly_of_{parameter}']].head())


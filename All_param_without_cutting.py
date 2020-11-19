"""
Разбивает дату на отдельные  столбцы (Год, Месяц, День).
Разбивает оригинальный файл БД по месяцам и годам
Затем в каждом отдельном файле:
    1. Меняет пустые (и неверные) значения глубины места (zz) на глубину последнего горизонта.
    2. Удаляет строки с пустыми значениями температур, солености, кислорода
    3. Фильтрует "выбросы" в показаниях температуры и солености, кислорода
    4. Прописывает номер станции

Затем объединяет все файлы в один файл!

"""
# todo DATETIME
# todo УБРАТЬ ВЫБРОСЫ В СОЛЕНОСТИ И ТЕМПЕРАТУРЕ И КИСЛОРОДЕ
# todo Поменять местами соленость и температуру в некоторых местах
# todo УДАЛИТЬ ВЫБРОСЫ В СОЛНОСТИ И ПРОВЕРИТЬ ОСТАЛЬНЫЕ И ЗАНОВО ПРОПИСАТЬ НОМЕРА СТАНЦИЙ


import pandas as pd


path_orig = 'C:/Users/Egor/Desktop/oxygen_2.0.1/All_parameters_without_none_extremum.csv'
orig_df = pd.read_csv(path_orig, delimiter=',')
#df_last = pd.read_csv('C:/Users/Egor/Desktop/oxygen_2.0.1/1930_6_nst.csv', delimiter=',')
#path_cutter = 'C:/Users/Egor/Desktop/all_parameters_okhotskoe/1930_01.csv'

def cutter_orig_file(df):
    """
    РАЗБИВАЕТ ОРИГИНАЛ ФАЙЛА НА НЕСКОЛЬКО ПО ГОДУ И МЕСЯЦУ
    """
    # new_df = pd.read_csv('C:/Users/Egor/Desktop/all_parameters_okhotskoe/new_orig_copy.csv', delimiter=',')
    # ДОБАВИТЬ ФАЙЛ ДЛЯ СОЕДИНЕНИЯ!!!!!!!!!!!!!!
    df_last = pd.read_csv('C:/Users/Egor/Desktop/oxygen_2.0.1/1930_6_nst.csv', delimiter=',')

    for year in range(1930, 2016):
        if year in list(df['Year']):
            for month in range(1, 13):
                if month in list(df.query('Year == @year')['Month']):
                    for day in range(1,32):
                        if day in list(df.query('Year == @year & Month == @month')['Day']):
                            df_new = df.query('Year == @year & Month == @month & Day == @day')
                            print('KK')
                            # !!!!!!!!!!!!!!!!!!!!!!!!NEW
                            #cleaning_cuttered_files(df_new)
                            df_new = df_new.drop_duplicates(['long', 'lat', 'level'])
                            # ВСТАВИТЬ НОМЕРА СТАНЦИЙ
                            number_station(df_new)
                            df_last = pd.concat([df_last, df_new])
                            df_last.to_csv('C:/Users/Egor/Desktop/oxygen_2.0.1/1930_6_nst.csv', index=False)

                            print('Cleaning_cuttered_files - OK')
                            print(f'{year, month, day}')



                    #print(df_new)
                    #number_station(df)
                    #print(df)
                    #df_last = pd.concat([df_last, df])
                    #print('KK')
    #df_last.to_csv('C:/Users/Egor/Desktop/all_parameters_okhotskoe/cutter/joined/1930_6_nst.csv',index=False)
    #print('joiner_clean_files - OK')




def cleaning_cuttered_files(df):
    df_last = pd.read_csv('C:/Users/Egor/Desktop/oxygen_2.0.1/1930_6_nst.csv', delimiter=',')
    """
    Берет отдельные файлы и меняет в каждом пустой zz на глубину последнего горизонта
    """
    #df_clean = df.copy()
    #df_clean['zz'] = df_clean['zz'].fillna(0) # Заменяю пустые значения в zz на 0
    """
        Замена глубины места(zz) на последний горизонт, в случае если она равна 0 
        или меньше глубины посл.горизонта
    """

    #grouped_by_coord = df.groupby(by=['long', 'lat'])  # Группирую по координтам
    #replaced_null_df = dict(list(grouped_by_coord))  # Записывая результат в словарь

    #for k, v in replaced_null_df.items():  # k,v - ключ и значение к словарю, соответственно
    #    max = v['level'].max()  # беру за максимум глубину последнего горизонта
    #    # Если глубина места меньше глубины последнего горизонта, соответственно заменяет ее
    #    for zz in v['zz']:
    #        if zz < max:
    #            v['zz'].replace(zz, max, inplace=True)
    #    # Если глубина места 0, заменяет ее на глубину последнего горизонта
     #   v['zz'].replace(0, max, inplace=True)
    # Достаю из словаря новые значения глубины места zz и в итоге записываю их в отдельный список
    #lst_zz = []
    #for v in replaced_null_df.values():
    #    lst_zz.append(v['zz'])

    #new_lst_zz = []
    #for zz in lst_zz:
    #    new_lst_zz.append(list(zz))

    #finished_lst_zz = []
    #for zz in new_lst_zz:
    #    for z in zz:
    #        finished_lst_zz.append(z)

    # Создаю из созданного списка со значениями zz новую таблицу
    #zz_df = pd.DataFrame(finished_lst_zz,
     #                    index=[i for i in range(len(finished_lst_zz))])  # DF с новыми глубина без 0

    # Записываю новые глубины в исходную таблицу
    #df['zz'] = zz_df
    #df['zz'] = finished_lst_zz
    # Запись промежуточного варианта
    # df.to_csv('C:/Users/Egor/Desktop/all_parameters_okhotskoe/cutter/' + f'{year}_{month}_1.csv', index=False)
    """
    Удаление строк с пустыми значениями и нулями в кислороде
    """
    #df = df.dropna()
    #df = df.query('oxig != 0')
    # Запись промежуточного варианта
    # df.to_csv('C:/Users/Egor/Desktop/all_parameters_okhotskoe/cutter/' + f'{year}_{month}_without_Nan_0.csv', index=False)

    """
    Удаление выбросов в температуре и солености
    """
    #df = df.query('sal < 40 & sal != 0 & temp < 40')

    #df.to_csv('C:/Users/Egor/Desktop/all_parameters_okhotskoe/cutter/' + f'{year}_{month}_without_Nan_0_Extremal.csv',
    #          index=False)

    df = df.drop_duplicates(['long', 'lat', 'level'])
    df_last = pd.concat([df_last, df])
    df_last.to_csv('C:/Users/Egor/Desktop/oxygen_2.0.1/1930_6_nst.csv', index = False)

    print('Cleaning_cuttered_files - OK')




def number_station(df):
    """
    ДОБАВЛЯЮ НОМЕРА СТАНЦИЙ
    """
    df_new = df.copy()
    nst = 1

    grouped_df = df_new.groupby(by=['long', 'lat'])  # Группирую по координатам
    grouped_df_series = grouped_df.size()  # Смотрю на результат объединения (сколько горизонтов на каждой станцийи)
    nums = grouped_df_series.shape[0]  # Кол-во станций

    lst = []
    # nst = last_station()  # Номер станции
    for i in range(nums):
        a_lst = [nst] * grouped_df_series.iloc[i]  # Список в котором номер станций, повторяющийся n-раз
        for num in a_lst:  # Из списка с номерами станций выписываю номера в отдельный список
            lst.append(num)
        nst += 1  # Увеличиваю порядковый номер станции

    df_new['Stations'] = lst  # Добавляю в таблицу столбец с номерами станций
    #path_df_with_nst = 'C:/Users/Egor/Desktop/all_parameters_okhotskoe/cutter/nst/' + f'{year}_{month}_nst.csv'
    #df.to_csv(path_df_with_nst, index=False)
    print('number_station - OK')
    return df_new




#cutter_orig_file(orig_df)

"""
 удаляет дубликаты во всем массиве

"""
def del_dubl_in_month():
    df_last = pd.read_csv('C:/Users/Egor/Desktop/oxygen_2.0.1/1930_6_nst.csv', delimiter=',')
    df_last = df_last.drop_duplicates(['long', 'lat', 'level', 'temp','sal', 'oxig'])
    #print(df_last.describe())
    df_last.to_csv('C:/Users/Egor/Desktop/oxygen_2.0.1/1930_6_nst_2.csv', index=False)
#del_dubl_in_month()


# if __name__ == '__main__':
    # cutter_orig_file()
    # new_date()
    # cleaning_cuttered_files()
    # number_station()
    # Перед выполнением joiner_clean_files() скопировать 1930_6_nst из nst в joined
    # joiner_clean_files()


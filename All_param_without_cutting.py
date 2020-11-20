"""

Разбивает оригинальный файл БД  Год --> Месяц --> День
Затем в каждом отдельном файле:
    1. Меняет пустые (и неверные) значения глубины места (zz) на глубину последнего горизонта.
    2. Удаляет строки с пустыми значениями температур, солености, кислорода
    3. Фильтрует "выбросы" в показаниях температуры и солености, кислорода
    4. Удаляет дубликаты в каждом дне
    5. Прописывает номер станции
    6. Удаляет дубликаты во всем массиве

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
    Выделяет из всей выборки данные по одному дню и дальше обрабатывает их, затем собирает все дни в один файл
    """

    df_last = orig_df[:1].copy()  # Пустой Датафрейм с заголовками для присоединения изменённых данных

    for year in list(df['Year'].unique()):
        for month in list(df.query('Year == @year')['Month'].unique()):
            for day in list(df.query('Year == @year & Month == @month')['Day'].unique()):
                df_new = df.query('Year == @year & Month == @month & Day == @day')  # Выборка по дню

                # cleaning_cuttered_files(df_new)

                # Если в одном дню станции повторились (даже если разные показатели t/s/o) удаляет второй дубль
                df_new = df_new.drop_duplicates(['long', 'lat', 'level'])

                # Вызов функции прописывания номеров станциям
                number_station(df_new)

                # Записывает обработанный день в пустой датафрейм, в котором только заголовки.
                df_last = pd.concat([df_last, df_new])

                print(f'{year, month, day}')
    # Записывает полученный датафрейм в csv
    df_last.to_csv('C:/Users/Egor/Desktop/oxygen_2.0.1/20_11_20_12_47(3).csv', index=False)


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
    Добавляет номер станции, с учетом номера станции в предыдущий день (сквозная нумерация)
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
    return df_new




def del_dubl_in_month():

    """
     Удаляет дубликаты во всем массиве
    """

    df_last = pd.read_csv('C:/Users/Egor/Desktop/oxygen_2.0.1/20_11_20_12_47(3).csv', delimiter=',')
    df_last = df_last.drop_duplicates(['long', 'lat', 'level', 'temp', 'sal', 'oxig'])
    print('OK')
    df_last.to_csv('C:/Users/Egor/Desktop/oxygen_2.0.1/20_11_20_12_47(4).csv', index=False)


if __name__ == '__main__':
    # cutter_orig_file(orig_df)
    # del_dubl_in_month()
    # cutter_orig_file()
    # new_date()
    # cleaning_cuttered_files()
    # number_station()
    # Перед выполнением joiner_clean_files() скопировать 1930_6_nst из nst в joined
    # joiner_clean_files()


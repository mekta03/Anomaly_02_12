import pandas as pd
# todo: РАЗОБРАТЬСЯ С ДАТОЙ
# todo: ПОРЯДОК ЗАПИСИ КОЛОНОК (КАК В ODV)
# todo: ПУСТЫЕ ЗНАЧЕНИЯ  T S УДАЛИТЬ и НОЛЬ у кислорода
# todo: СДЕЛАТЬ НЕСКОЛЬКО ВЕРСИЙ, c S T Oxig
# todo: КОЛ-ВО СТАНЦИЙ, ПРАВИЛЬНО ЛИ ПОЛУЧИЛОСЬ?????!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# todo: Разбить по месяцам и годам ?????!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# todo: Переименовать переменные в функции вытаскивания значений zz
# todo: Отфильтровать значения по одинаковым горизонтам (сделать выборку с наиболее часто встреч горизонтами)

path_bd = 'C:/Users/Egor/Desktop/test_oxig/2015.csv'
path_ox_with_nst = 'C:/Users/Egor/Desktop/test_oxig/со_станциями_вручную.csv'
path_finished_file = 'C:/Users/Egor/Desktop/test_oxig/New/2015_new.csv'

df_2015 = pd.read_csv(path_bd, header=0, delimiter=',')
df_2015 = df_2015.drop(['Unnamed: 0'], axis=1)  # Удаляю какой-то "левый" столбец
df_2015['zz'] = df_2015[['zz']].fillna(0)


new_df_2015 = df_2015.groupby(by=['long', 'lat'])   # Группирую по координатам
new_df_2015_series = new_df_2015.size()     # Смотрю на результат объединения (сколько горизонтов на каждой  станцийи)
nums = new_df_2015_series.shape[0]      # Колво станций


def last_station():
    path_last = 'C:/Users/Egor/Desktop/test_oxig/New/df_last.csv'
    df_last = pd.read_csv(path_last, header=0, delimiter=',')
    nst = df_last['Stations'].max()
    nst += 1
    return nst


lst = []
nst = last_station()    # Номер станции
for i in range(nums):
    a_lst = [nst]*new_df_2015_series.iloc[i]    # Список в котором номер станций, повторяющийся n-раз
    for num in a_lst:                           # Из списка с номерами станций выписываю номера в отдельный список
        lst.append(num)
    nst += 1                                    # Увеличиваю порядковый номер станции

df_2015['Stations'] = lst                       # Добавляю в таблицу столбец с номерами станций

gr_by_nst = df_2015.groupby(by=['Stations'])    # Группирую по станциям

replaced_null_df = dict(list(gr_by_nst))    # Переношу сгруппированную таблицу в словарь


def replaced_zeroes():
    """
    Заменяет глубину места(zz) на последний горизонт, в случае если она равна 0 или меньше глубины посл.горизонта
    """
    for k, v in replaced_null_df.items():      # k,v - ключ и значение к словарю, соответственно
        max = v['level'].max()                 # беру за максимум глубину последнего горизонта
        # Если глубина места меньше глубины последнего горизонта, соответственно заменяет ее
        for zz in v['zz']:
            if zz < max:
                v['zz'].replace(zz, max, inplace=True)
        # Если глубина места 0, заменяет ее на глубину последнего горизонта
        v['zz'].replace(0, max, inplace=True)
    # Достаю из словаря новые значения глубины места zz и в итоге записываю их в отдельный список
    lst_zz = []
    for v in replaced_null_df.values():
        lst_zz.append(v['zz'])

    new_lst_zz = []
    for zz in lst_zz:
        new_lst_zz.append(list(zz))

    finished_lst_zz = []
    for zz in new_lst_zz:
        for z in zz:
            finished_lst_zz.append(z)

    # Создаю из созданного списка со значениями zz новую таблицу
    zz_df = pd.DataFrame(finished_lst_zz, index=[i for i in range(len(finished_lst_zz))]) # DF с новыми глубина без 0
    df_2015_copy = df_2015.copy()
    # Записываю новые глубины в исходную таблицу
    df_2015_copy['zz'] = zz_df
    df_2015_copy.to_csv(path_finished_file, index=False)


def joiner():
    """
    Объединяет разбитые по годам файлы
    """
    # Сначала прописываешь в путь файл с первым годом (1930) а затем к нему уже плюсуешь остальные

    path_last = 'C:/Users/Egor/Desktop/test_oxig/New/df_last.csv'
    path_new = 'C:/Users/Egor/Desktop/test_oxig/New/2015_new.csv'

    df_last = pd.read_csv(path_last, header=0, delimiter=',')
    df_new = pd.read_csv(path_new, header=0, delimiter=',')

    df_last = pd.concat([df_last, df_new])
    df_last.to_csv('C:/Users/Egor/Desktop/test_oxig/New/df_last.csv', index=False)
    print(df_last)


# last_station()
# replaced_zeroes()
# joiner()

print('OK')

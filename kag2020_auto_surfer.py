"""
Интерполяция методом Kriging при помощи Surfer

Полный набор действий:
    Запустить Surfer от имени Админа
    Интерполирую auto_surfer.py
    Если надо бланкировать прописать путь к bln и выбрать в blank True
    
    Можно через scripts
    Через script Blank_all бланкирую все grd
    Через script grd_to_dat конвертирую grd в dat
    Обрабатываю dat через python dat_to_csv.py
"""
# Если ошибка: AttributeError: module win32com.gen_py.54C3F9A2-980B-1068-83F9-0000C02A351Cx0x1x9
# has no attribute CLSIDToClassMap,
# то надо удалить папку gen_py 'C:\Users\malyg\AppData\Local\Temp\gen_py'

# TODO сделать exception в случае ошибки если не запустил surfer
# TODO КОЛОНКА Latitude Longitude предупреждение либо поиск

import win32com.client 
import pandas as pd


def surfer_interpolation(input_file, output_file, range_coordinates, range_columns):
    
    """
    ! WARNING ! Surfer должен быть запущен \n
    input_file - csv, из которого берутся данные для интерполяции; \n
    output_file - название файла без расширения, в который будут записаны результаты интерполяции; \n
    range_coordinates - список координат и дискретность [x_min, x_max, y_min, y_max, spacing] [134.5, 164.5, 49.5, 61.5, 0.5]; \n
    range_columns - диапазон колонок для интерполяции (результат), \n 
                    может быть списком из колонок, или целым числом; \n


    Делает интерполяцию в Surfer метод Kriging
    Выходной файл в dat формате
    """

    x_min, x_max = range_coordinates[0], range_coordinates[1]
    y_min, y_max = range_coordinates[2], range_coordinates[3]
    spacing = range_coordinates[4]
  
    DataFile = input_file

    df = pd.read_csv(input_file, sep=',')
    col_1 = df.columns.get_loc("Longitude")+1
    col_2 = df.columns.get_loc("Latitude")+1

    start_range = range_columns

    # Проверка: интерполирует отдельные колонки, или какой-то диапазон.
    if type(start_range) != list:
        start_range = [start_range]

    for col_3 in start_range:

        OutFile = f"{output_file}_{col_3}"
        app = win32com.client.gencache.EnsureDispatch('Surfer.Application')
        # app = win32com.client.Dispatch('Surfer.Application')

        app.GridData(DataFile=DataFile,
                    # Номера колонок
                    xCol = col_1, yCol = col_2, zCol = col_3,
                    Algorithm = win32com.client.constants.srfKriging,
                    # Spacing 
                    NumCols = ((x_max-x_min)/spacing) + 1,
                    NumRows = ((y_max-y_min)/spacing) + 1,
                    xMin = x_min, xMax = x_max, yMin = y_min, yMax = y_max, ShowReport=False,
                    # OutFmt = win32com.client.constants.srfGridFmtXYZ, #grd
                    OutFmt = win32com.client.constants.srfGridFmtBinary, #dat
                    OutGrid = OutFile,
                    )
        if blank:
            app.GridBlank(InGrid=OutFile, BlankFile=bln_file, OutGrid=OutFile, OutFmt=3,)

            app.GridConvert(InGrid=OutFile, OutGrid=OutFile, OutFmt=win32com.client.constants.srfGridFmtXYZ)


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

#  Бланкирование #! bln - при digitilize в опции убрать галку NoData inside (тогда данные внутри - иначе снаружи)
bln_file = 'D:/Life/Работа/ТИНРО/Текущие проекты/Kaganovsky_2020/kag_64/n_zk.bln'
blank = True

for lvl in [*std_lvl, 'last_lvl']:
    input_file = f'D:/Life/Работа/ТИНРО/Текущие проекты/Kaganovsky_2020/kag_64/csv_new_2/csv/{lvl}.csv'
    output_file = f'D:/Life/Работа/ТИНРО/Текущие проекты/Kaganovsky_2020/kag_64/csv_new_2/dat/{lvl}'

    # Координаты и дискретность координат x_min, x_max, y_min, y_max, spacing
    x_y_spacing = [134.5, 164.5, 49.5, 61.5, 0.5]

    # Так как NO3 на 1000 метров нет, то её исключаем
    
    if lvl == 'last_lvl' or lvl < 1000:
        col_range = [*range(11, 21)]
    else:
        col_range = [*range(11, 20)]

    surfer_interpolation(input_file, output_file, x_y_spacing, col_range)


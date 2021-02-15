import win32com.client 
import pandas as pd

i = range(18,19)
print(*i)
# df=pd.DataFrame(data={
#                         'latidute':[0,1,2,3,4,5],
#                         'longitude':[0,1,2,3,4,5],
#                         'temp':[3,3,3,3,3,3]
#                     }, index = [i for i in range(6)]
#                     )
# print(df.columns.get_loc("temp"))

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

    # x_min, x_max = 120, 180
    # y_min, y_max = 30, 70
    # spacing = 0.01
    
    DataFile = input_file
    
    df = pd.read_csv(input_file, sep=',')
    col_1 = df.columns.get_loc("Longitude")+1
    col_2 = df.columns.get_loc("Latitude")+1
    print(col_1)
    
    start_range = range_columns
    
    # Проверка: интерполирует отдельные колонки, или какой-то диапазон.
    if type(start_range) != list:
        start_range = [start_range]

    for col_3 in start_range:
        print('col_3')
        print(col_3)
        
        OutFile = f"{output_file}_{col_3}"
        
        app = win32com.client.gencache.EnsureDispatch('Surfer.Application')
        # print(help(app.GridData))
        app.GridData(DataFile=DataFile,
                    # Номера колонок
                    xCol = col_1, yCol = col_2, zCol = col_3,
                    Algorithm = win32com.client.constants.srfKriging,
                    # Spacing 
                    NumCols = ((x_max-x_min)/spacing) + 1,
                    xMin = x_min, xMax = x_max, yMin = y_min, yMax = y_max, ShowReport=False,
                    OutFmt = win32com.client.constants.srfGridFmtXYZ, # dat
                    # OutFmt = win32com.client.constants.srfGridFmtBinary, #grd
                    OutGrid = OutFile,
                    )


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


for lvl in std_lvl:
    input_file = f'D:/Life/Работа/ТИНРО/Текущие проекты/Kaganovsky_2020/kag_64/csv/csv/{lvl}.csv'
    output_file = f'D:/Life/Работа/ТИНРО/Текущие проекты/Kaganovsky_2020/kag_64/csv/dat/{lvl}'

    # Координаты и дискретность координат x_min, x_max, y_min, y_max, spacing
    x_y_spacing = [134.5, 164.5, 49.5, 61.5, 0.5]

    # Так как NO3 на 1000 метров нет, то её исключаем
    if lvl < 1000:
        col_range = [*range(11, 21)]
    else:
        col_range = [*range(11, 18),19,20]
    # col_range = [*range(11, 12)]
    # col_range = 11

    surfer_interpolation(input_file, output_file, x_y_spacing, col_range)














# file_csv =r'D:\Life\Работа\ТИНРО\Текущие проекты\Kaganovsky_2020\kag_64\csv\csv\last_level.csv'
# surfer_interpolation(file_csv, 'last_level')


# name_of_parameters = ['dissolved_oxygen','nitrate', 'phosphat','silicate','salinity','temperature']

# dct_month = {1: 'January', 2: 'Febraury', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
#             9: 'September', 10: 'October', 11: 'November', 12: 'December'}

# path_dir_new = r'D:/Life/Работа/ТИНРО/Программы/Атласы (World Ocean Atlas)/test_anomaly/'


# for name in name_of_parameters:
#     if name not in ['salinity','temperature']:
#         for lvl in dct_month.keys():
#             print(lvl)
            
#             input_file = rf'{path_dir_new}{name}/woa18_{name}_{lvl}.csv'
#             output_file = f'{path_dir_new}{name}/woa18_{name}_{lvl}'
#             surfer_interpolation(input_file,output_file, lvl, name)
#     else:
#         for lvl in dct_month.values():
#             name_of_month = lvl.lower()
#             file_csv = f'{path_dir_new}{name}/woa18_{name}_{name_of_month}.csv'
#             surfer_interpolation(file_csv, lvl)

# # file_csv =r'D:\Life\Работа\ТИНРО\Текущие проекты\Kaganovsky_2020\kag_64\csv\csv\last_level.csv'
# # surfer_interpolation(file_csv, 'last_level')


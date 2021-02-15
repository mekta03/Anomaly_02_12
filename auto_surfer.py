import win32com.client 
import pandas as pd

def surfer_interpolation(file_csv, level, name_dir):
    """
    ! Surfer должен быть запущен
    Делает интерполяцию в Surfer метод Kriging
    Выходной файл в dat формате
    """
    # x_min, x_max = 134.5, 164.5
    # y_min, y_max = 49.5, 61.5
    # spacing = 0.5
    x_min, x_max = 120, 180
    y_min, y_max = 30, 70
    spacing = 0.01
    
    # DataFile = r'C:\Users\malyg\Desktop\kag_64\dat\0.csv'
    DataFile = file_csv
    # TODO Перестроить в csv до разделения NO3 в конец
    col_1 = 2
    col_2 = 1
    df = pd.read_csv(file_csv, sep=',')
    print(level)

    last_col = len(df.columns)+1
    path_project = "D:/Life/Работа/ТИНРО/Текущие проекты/Kaganovsky_2020/kag_64/"
    # for col_3 in (range(12,20) if level < 1000 else range(12,19)):
    for col_3 in range(3,last_col):
        print(col_3)
    # for col_3 in range(20,21):
        # OutFile = rf"D:/Life/Работа/ТИНРО/Программы/Атласы (World Ocean Atlas)/test_anomaly/{name_dir}/woa_{name_dir}_{level}_{col_3}"
        OutFile = f"C:/Users/malyg/Desktop/anomal/{name_dir}/woa_{name_dir}_{level}_{col_3}"
        # OutFile = f"D:/Life/Работа/ТИНРО/Текущие проекты/Kaganovsky_2020/kag_64/csv/grd/{col_3}"
        app = win32com.client.gencache.EnsureDispatch('Surfer.Application')
        print(help(app.GridData))
        app.GridData(DataFile=DataFile,
                    # Номера колонок
                    xCol = col_1, yCol = col_2, zCol = col_3,
                    Algorithm = win32com.client.constants.srfKriging,
                    # Spacing 
                    NumCols = ((x_max-x_min)/spacing) + 1,
                    NumRows = ((y_max-y_min)/spacing) + 1,
                    xMin = x_min, xMax = x_max, yMin = y_min, yMax = y_max, ShowReport=False,
                    OutFmt = win32com.client.constants.srfGridFmtXYZ,
                    # OutFmt = win32com.client.constants.srfGridFmtBinary,
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


# for lvl in std_lvl:
#     file_csv = f'D:/Life/Работа/ТИНРО/Текущие проекты/Kaganovsky_2020/kag_64/csv/csv/{lvl}m.csv'
#     surfer_interpolation(file_csv, lvl)

# file_csv =r'D:\Life\Работа\ТИНРО\Текущие проекты\Kaganovsky_2020\kag_64\csv\csv\last_level.csv'
# surfer_interpolation(file_csv, 'last_level')


name_of_parameters = ['dissolved_oxygen','nitrate', 'phosphat','silicate','salinity','temperature']

dct_month = {1: 'January', 2: 'Febraury', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
            9: 'September', 10: 'October', 11: 'November', 12: 'December'}

path_dir_new = r'D:/Life/Работа/ТИНРО/Программы/Атласы (World Ocean Atlas)/test_anomaly/'


for name in name_of_parameters:
    if name not in ['salinity','temperature']:
        for lvl in dct_month.keys():
            file_csv = rf'{path_dir_new}{name}/woa18_{name}_{lvl}.csv'

            surfer_interpolation(file_csv, lvl, name)
    else:
        for lvl in dct_month.values():
            name_of_month = lvl.lower()
            file_csv = f'{path_dir_new}{name}/woa18_{name}_{name_of_month}.csv'
            surfer_interpolation(file_csv, lvl)

# file_csv =r'D:\Life\Работа\ТИНРО\Текущие проекты\Kaganovsky_2020\kag_64\csv\csv\last_level.csv'
# surfer_interpolation(file_csv, 'last_level')



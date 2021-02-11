"""
Переводит dat файлы в xlsx
"""

import pandas as pd
import openpyxl
import os


# Границы уровней
dct_1 = {i: i + 9 for i in range(0, 31, 10)}
dct_2 = {i: i + 19 for i in range(30, 31)}
dct_3 = {i: i + 24 for i in range(50, 99, 25)}
dct_4 = {i: i + 49 for i in range(100, 251, 50)}
dct_5 = {i: i + 99 for i in range(300, 600, 100)}
dct_6 = {i: i + 99 for i in range(600, 1001, 200)}
# dct_6 = {i: i + 99 for i in range(600, 1000, 200)}

dct_std_lvl = {**dct_1, **dct_2, **dct_3, **dct_4, **dct_5, **dct_6 }
std_lvl = [*dct_std_lvl.keys()]

path_project = 'C:/Users/malyg/Desktop/kag_64/csv/dat/'
name_xlsx = 'result.xlsx'
first_run = True


def excel(df, sheet_name, file_name, mode):
    """
    Записывает данные в xlsx
    \n df - данные для записи
    \n sheet_name -  имя листа
    \n file_name - имя файла xlsx
    \n mode - режим записи, w-перезапись, a-добавление
    """

    df_to_xlsx = df.copy()
    name_sheet = sheet_name
    name_xlsx = file_name
    global first_run

    if os.path.exists(file_name):

        if first_run:
            mode_xlsx = 'w'
            first_run = False
        else:
            mode_xlsx = mode
    else:
        mode_xlsx = 'w'
        first_run = False
    # Путь записи файла
    path_xlsx = name_xlsx

    with pd.ExcelWriter(path_xlsx, engine='openpyxl', mode=mode_xlsx) as writer:
        df_to_xlsx.to_excel(writer, index=False, sheet_name=f'{name_sheet}')

    # Удаляет ненужный пустой лист, который был нужен для создания xlsx
    if mode == 'a':
        wb = openpyxl.load_workbook(path_xlsx)
        sheet = wb.sheetnames

        if '1' in sheet:
            pfd = wb['1']
            wb.remove(pfd)
            wb.save(path_xlsx)


df_concated_all_lvl = pd.DataFrame()
for lvl in std_lvl:
    df_concated = pd.DataFrame()

    #
    flag=True

    # for col_3 in range(12,20):
    for col_3 in (range(12,20) if lvl < 1000 else range(12,19)):
        file = f"{path_project}{lvl}_{col_3}_blanked.dat"
                                   
        name_of_clolumn = {12:'Temperature', 13:'Salinity', 14:'O2', 15:'O2_%', 16:'Si', 17:'PO4', 18:'NO2', 19:'NO3'}

        columns = ['long', 'lat', name_of_clolumn[col_3]]
        dff = pd.read_csv(file, sep=' ', engine='python', names=columns)
        dff = dff.copy()
        dff[name_of_clolumn[col_3]] = dff[name_of_clolumn[col_3]].round(3)
        if flag == True:
            flag = False
            df_concated = pd.concat([df_concated, dff])
        else:
            df_concated = pd.merge(df_concated, dff, on=['long', 'lat'])

    excel(df_concated, lvl, f'{path_project}{name_xlsx}', 'a')

    df_concated['level'] = lvl
    df_concated_all_lvl = pd.concat([df_concated_all_lvl, df_concated])
    
    # df_concated.to_csv( f"path_project{lvl}_.csv", index=False)
df_concated_all_lvl = df_concated_all_lvl[['long','lat','level','Temperature','Salinity','O2','O2_%','Si','PO4','NO2','NO3']]
df_concated_all_lvl.to_csv( f'{path_project}all_lvl.csv', index=False)


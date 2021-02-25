"""
Сначала обрезает файл атласа, потом берет проинтерполированный в Surfer атлас и фильтрует по нужным координатам
"""
#TODO:Не нужно ли заменить inner на outer
#TODO:Сделать выбор множественной обрезки или одного файла (количество месяцев и  их номера)

import pandas as pd

min_lat, max_lat = 30, 70
min_long, max_long = 120, 180

name_of_parameters = ['dissolved_oxygen','nitrate', 'phosphat','silicate','salinity','temperature']

# Paths and names of work`s files
path_dir = r'D:/Life/Работа/ТИНРО/Программы/Атласы (World Ocean Atlas)/test_anomaly/'



# path_dir = 'C:/Users/malyg/Desktop/test_anomaly/'
# path_dir = '/home/lenovo/test_anomaly_new/'

name_woa = ['interpolated_woa18_salinity_september.csv', 
            'interpolated_woa18_salinity_october.csv'
            ]

path_coord = f'{path_dir}Станции.csv'
dct_month = {1: 'January', 2: 'Febraury', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
            9: 'September', 10: 'October', 11: 'November', 12: 'December'}


def cutter(path_dir_woa, name):
    """
    Меняет заголовки в атласе\n
    Отбирает данные по заданным пределам координат,\n
    Отсекает ненужные горизонты !!! (пока закоментировано)\n
    и сохраняет полученный файл атласа

    """
    path_woa_original = path_dir_woa
    #TEST
    for i in range(1,13):
        # if i < 10:
        #     o = '0'
        # else:
        #     o = ''
        if name not in ['temperature', 'salinity']:
            path_woa_original_1 = f'{path_woa_original}woa18_{name}_{i}.csv'
        else:
            name_of_month = dct_month[i].lower()
            path_woa_original_1 = f'{path_woa_original}woa18_{name}_{name_of_month}.csv'
        # path_woa_original_1 = f'{path_woa_original}woa18_salinity_september.csv'

        # ! СМЕНИТЬ НАЗВАНИЕ НА woa_salinity_september

        # path_result_original = f'{path_woa_original}woa18_all_omn01_cutted_2.csv'
        
        # path_woa_original_1 = f'{path_woa_original}woa18_all_o'+f'{o}{i}mn01.csv'
        # path_result_original = f'{path_woa_original}woa18_all_o'+f'{o}{i}mn01_cutted.csv'

        woa_df = pd.read_csv(path_woa_original_1, header = 1, sep=',')

        new_woa_df = woa_df.rename(columns = {"#COMMA SEPARATED LATITUDE":'Latitude',' LONGITUDE':'Longitude',
                                          ' AND VALUES AT DEPTHS (M):0':'0'})

        new_woa_df = new_woa_df.query("( @min_lat <= Latitude  <= @max_lat ) and \
                                        (@min_long <= Longitude <= @max_long )")
                                        
        # list_of_columns = ['LATITUDE', 'LONGITUDE', '0', '20', '50', '100', '200', '500']
        # new_woa_df = new_woa_df[list_of_columns]
        new_woa_df.to_csv(path_woa_original_1, index=False)
  
    print('OKEY')


for name in name_of_parameters:
    path_dir_woa = f'{path_dir}{name}/'
    
    cutter(path_dir_woa, name)




def filtration(path_woa, path_coord, path_result):
    """

    Берет атлас, в котором данные были проинтерполированы с помощью Surfer и файл с координатами станций,
    и отбирает данные в атласе по координатам станций,
    затем записывает результат в отдельный файл.

    """

    # Load files of WOA and station`s coordinates
    woa_df = pd.read_csv(path_woa, sep=',')
    coord_df = pd.read_csv(path_coord, sep=',')

    # Merge files by only common coordinates and write result to new file
    rslt_df = pd.merge(coord_df, woa_df, on=['Latitude', 'Longitude'], how='inner')
    rslt_df = rslt_df.drop(['Date', 'Time'], axis=1).round(2)

    print(rslt_df.head())
    
    rslt_df.to_csv(path_result, index=False)




def filtration_all():
    for name in name_woa:
        full_path = path_dir + name
        path_rslt = f'{path_dir}filtered_{name}'
        filtration(full_path, path_coord, path_rslt)


if __name__ == '__main__':
    # filtration_all()
    # cutter()
    pass


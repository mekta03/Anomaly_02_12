"""
Сначала обрезает файл атласа, потом берет проинтерполированный в Surfer атлас и фильтрует по нужным координатам
"""
#TODO:Не нужно ли заменить inner на outer

import pandas as pd

min_lat, max_lat = 42, 62
min_long, max_long = 135, 165


def cutter():
    """
    Меняет заголовки в атласе\n
    Отбирает данные по заданным пределам координат,\n
    Отсекает ненужные горизонты !!! (пока закоментировано)\n
    и сохраняет полученный файл атласа

    """
    path_woa_original = f'{path_dir}woa_originals/'
    #TEST
    for i in range(1,13):
        if i < 10:
            o = '0'
        else:
            o = ''

        path_woa_original_1 = f'{path_woa_original}woa18_all_o'+f'{o}{i}mn01.csv'
        path_result_original = f'{path_woa_original}woa18_all_o'+f'{o}{i}mn01_cutted.csv'

        print(i)
        print(path_woa_original_1)
        print(path_result_original)
        print()

        # if i < 10:
        #     path_woa_original = f'{path_woa_original}woa18_all_o0'+f'{i}mn01.csv'
        #     path_result_original = f'{path_woa_original}woa18_all_o0'+f'{i}mn01_cutted.csv'

        # else:
        #     path_woa_original = f'{path_woa_original}woa18_all_o'+f'{i}mn01.csv'
        #     path_result_original = f'{path_woa_original}woa18_all_o'+f'{i}mn01_cutted.csv'

        # woa_df = pd.read_csv(path_woa_original, header = 1, sep=',')

        # new_woa_df = woa_df.rename(columns = {"#COMMA SEPARATED LATITUDE":'LATITUDE',' LONGITUDE':'LONGITUDE',
        #                                   ' AND VALUES AT DEPTHS (M):0':0})

        # new_woa_df = new_woa_df.query("( @min_lat <= LATITUDE  <= @max_lat ) and \
        #                                 (@min_long <= LONGITUDE <= @max_long )")
                                        
        # #list_of_columns = ['LATITUDE', 'LONGITUDE', '0', '20', '50', '100', '200', '500']
        # #new_woa_1_df = new_woa_df[list_of_columns]
        # new_woa_df.to_csv(path_result_original, index=False)
  
    print('OKEY')


def filtration(path_woa, path_coord, path_result):
    """

    Берет атлас, в котором данные были проинтерполированы с помощью Surfer и файл с координатами станций,
    и отбирает данные в атласе по координатам станций,
    затем записывает результат в отдельный файл.

    """
    # for path in path_woa_list:

    # path_woa = path
    # Load files of WOA and station`s coordinates
    woa_df = pd.read_csv(path_woa, sep=',')
    coord_df = pd.read_csv(path_coord, sep=',')

    # Merge files by only common coordinates and write result to new file
    rslt_df = pd.merge(coord_df, woa_df, on=['Latitude', 'Longitude'], how='inner')
    rslt_df = rslt_df.drop(['Date', 'Time'], axis=1).round(2)

    print(rslt_df.head())
    
    rslt_df.to_csv(path_result, index=False)


# Paths and names of work`s files
path_dir = 'C:/Users/malyg/Desktop/test_anomaly/'
name_woa = ['interpolated_woa18_salinity_september.csv', 
            'interpolated_woa18_salinity_october.csv'
            ]

path_coord = f'{path_dir}Станции.csv'

def filtration_all():
    for name in name_woa:
        full_path = path_dir + name
        path_rslt = f'{path_dir}filtered_{name}'
        filtration(full_path, path_coord, path_rslt)


if __name__ == '__main__':
    # filtration_all()
    cutter()



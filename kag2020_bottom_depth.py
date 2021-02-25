import pandas as pd
import numpy as np


path = r'D:\Life\Работа\ТИНРО\Текущие проекты\Kaganovsky_2020\kag_64\all_lvl_date.csv'

df = pd.read_csv(path, sep=',')

# print(df.head())
# df_group = df.groupby(by=['long', 'lat'])
# print(df_group.get_group(('153','51')))
df_concat = pd.DataFrame()
for i in range(0, 378*16, 16):
    dff = df.iloc[i:i+16,:]
    num_st = dff['st'].unique()[0]
    depth = dff['bdepth'].unique()[0]
    dff = dff.copy()
    dff['Station'] = int(num_st)
    dff = dff.copy()
    dff['bottom_depth'] = depth
    dff = dff.copy()
    dff = dff.query('level < @depth')


    df_concat = pd.concat([df_concat, dff])
    print(num_st)


df_concat = df_concat.drop(['st', 'bdepth'], axis=1)

print(df_concat)
print()
print(df_concat.describe())
df_concat.to_csv(r'D:\Life\Работа\ТИНРО\Текущие проекты\Kaganovsky_2020\kag_64\all_result.csv', index=False)
# for lvl in sorted(df['level'].unique()):
#     dff = df.query('level == @lvl')
#     dff.to_csv(fr'D:\Life\Работа\ТИНРО\Текущие проекты\Kaganovsky_2020\kag_64\csv\csv\{lvl}_num_date.csv')
# lst_long = df['long'].unique()
# lst_lat = df['lat'].unique()

# print(lst_long)
# print()
# print(lst_lat)

# dct_coord = {}
# # dct_coord.keys, dct_coord.values = lst_long, lst_lat
# # for k,v in dct_coord.items():
# dct_coord = {k: v for k in lst_long for v in lst_lat}
# print(dct_coord)

# # TODO СОртировать по координатам из словаря и по уровню




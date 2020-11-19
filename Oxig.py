"""

Работа с БД по кислороду

"""

import pandas as pd

path_bd = 'C:/Users/Egor/Desktop/test_oxig/oxig_copy.csv'
path_ox_with_nst = 'C:/Users/Egor/Desktop/test_oxig/со_станциями_вручную.csv'

oxig_orig_df = pd.read_csv(path_bd, delimiter=',')
new_oxig_df = oxig_orig_df.copy()
new_oxig_df = new_oxig_df.drop(['Unnamed: 1'], axis=1)
sort_oxig_df = new_oxig_df.sort_values(by=['long', 'lat', 'data'])

grouped_df = sort_oxig_df.groupby(['long', 'lat', 'data'])

df_size = grouped_df.size()
lst_size = list(df_size.values)


df_oxig_with_nst = pd.read_csv(path_ox_with_nst, delimiter=',')
df_oxig_with_nst1 = df_oxig_with_nst.groupby(['Stations'])

dict_oxig_with_nst1 = dict(list(df_oxig_with_nst1))
#print(dict_oxig_with_nst1.values())


#Создаю новый датафрейм с глубина мест (заменяют ноль на макс знач горизонтов)
def foo():
    for k, v in dict_oxig_with_nst1.items():
        max = v['level'].max()
        v['zz'].replace(0, max, inplace=True)

    lst1212 = []
    for v in dict_oxig_with_nst1.values():
        lst1212.append(v['zz'])

    lst333 = []
    for i in lst1212:
        lst333.append(list(i))

    lst444 = []
    for i in lst333:
        for z in i:
            lst444.append(z)

    zz_df = pd.DataFrame(lst444, index= [i for i in range(len(lst444))])

    #zz_df.to_csv('C:/Users/Egor/Desktop/test_oxig/zz.csv')

foo()





# Создаю датафрейм с номерами станций повторяющиеся кол-во раз, равное кол-во горизонтов
def nst():
    lst_full =[]
    z = 1
    for i in lst_size:
        lst_full.append([z]*i)
        z += 1

    nums = []
    for i in lst_full:
        for y in i:
            nums.append(y)

    nst_df = pd.DataFrame(nums)
    return nst_df


stations = nst()
stations_df = stations.copy()
#stations_df.to_csv('C:/Users/Egor/Desktop/test_oxig/nst.csv')
"""
path_ox_with_nst = 'C:/Users/Egor/Desktop/test_oxig/со_станциями_вручную.csv'
df_oxig_with_nst = pd.read_csv(path_ox_with_nst, delimiter=',')
new_oxig_df1 = df_oxig_with_nst.query('Stations == 1')
num = 10
new_oxig_df1['new_zz'] = [10, 10, 10]
"""
#print(new_oxig_df1)

"""
#8643
for i in range(5):
    df_oxig_with_nst.query('Stations == @i')
    #print(df_oxig_with_nst.query('Stations == @i')['zz'].mean())
    a = df_oxig_with_nst.query('Stations == @i')['zz'].mean()
    if a != 1:
        df_oxig_with_nst.query('Stations == @i')['zz'] = 0
        print('zzzzz')

"""

#sort_oxig_df['Stations'] = stations_df
#print(sort_oxig_df)
#sort_oxig_df.to_csv('C:/Users/Egor/Desktop/test_oxig/sorted.csv')

"""
for (k1, k2,k3), group in grouped_df:
    print(k1, k2, k3)
    print(group)
    """

dict_oxig = dict(list(grouped_df))
#print(list(dict_oxig.keys()))
#new_dff = pd.DataFrame(dict_oxig, index=[i for i in range(len(dict_oxig))])

#print(dict_oxig[(139.0, 55.100002, '03.06.2002')])

"""
КОЛ_ВО СТАНЦИЙ
"""
z = 0
for k in dict_oxig.keys():
    #print(k)
    z += 1
    #print(z)


#lst1 = [(0,1),(2,3),(4,5)]
#dict_lst1 = dict(lst1)
#print(dict_lst1[4])
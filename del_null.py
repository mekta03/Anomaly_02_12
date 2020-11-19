"""
Удаляет пустые значения и нули (полностью строки)
"""
import pandas as pd


path_df_last = 'C:/Users/Egor/Desktop/df_last.csv'
new_df_last = pd.read_csv(path_df_last, delimiter=',')

new_df_last2 = new_df_last.dropna()

#new_df_last2.to_csv('C:/Users/Egor/Desktop/df_last_new.csv')
new_df_last3 = new_df_last2.query('oxig != 0')
new_df_last3.to_csv('C:/Users/Egor/Desktop/df_last_new_oxig.csv')
print(new_df_last3)



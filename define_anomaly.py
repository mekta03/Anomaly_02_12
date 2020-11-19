"""
Расчитывает аномалии между фактическими значениями и WOA проинтерполированными в Surfer
"""

import pandas as pd

path_original = 'C:/Users/Egor/Desktop/test_anomaly/test_test/to_ODV.csv'

woa_1 = 'Salinity_WOA_September'
woa_2 = 'Salinity_WOA_October'

df_original = pd.read_csv(path_original, delimiter=',')

df_new = df_original.copy()
grad = (df_new[woa_2] - df_new[woa_1])/30
#print(grad)
query1 = 'Day >= 15 and Month == 9'
query2 = 'Day <= 15 and Month == 10'

df_query_1 = df_new.query(query1)
df_query_2 = df_new.query(query2)

mean_for_date_1 = df_query_1[woa_1] + ((df_query_1['Day'] - 15) * grad)
mean_for_date_2 = df_query_2[woa_2] + ((df_query_2['Day'] - 15) * grad)
print(mean_for_date_1)
anomaly_1 = (df_query_1['Salinity'] - mean_for_date_1).dropna()
anomaly_2 = (df_query_2['Salinity'] - mean_for_date_2).dropna()

finished_df = pd.concat([anomaly_1, anomaly_2],ignore_index=True)

df_new['Anomaly'] = finished_df
df_new.to_csv('C:/Users/Egor/Desktop/test_anomaly/test_test/to_ODV_with__anomaly.csv', index=False)

#print(df_new)



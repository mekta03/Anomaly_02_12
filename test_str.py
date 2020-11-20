import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")

df = pd.read_csv('C:/Users/Egor/Desktop/oxygen_2.0.1/All_parameters_without_none_extremum.csv', delimiter=',')
df_new1 = pd.read_csv('C:/Users/Egor/Desktop/oxygen_2.0.1/1930_6_nst.csv', delimiter=',')
df_new2 = pd.read_csv('C:/Users/Egor/Desktop/oxygen_2.0.1/1930_6_nst_2.csv', delimiter=',')
df_new3 = pd.read_csv('C:/Users/Egor/Desktop/oxygen_2.0.1/20_11_20_12_47.csv', delimiter=',')
df_new4 = pd.read_csv('C:/Users/Egor/Desktop/oxygen_2.0.1/20_11_20_12_47(2).csv', delimiter=',')
df_new5 = pd.read_csv('C:/Users/Egor/Desktop/oxygen_2.0.1/20_11_20_12_47(3).csv', delimiter=',')

print(df_new1.describe())
print(df_new2.describe())
print(df_new3.describe())
print(df_new4.describe())
print(df_new5.describe())


month = 5
#print(df_new2.query('Year == 1949 &  83 <= Stations <= 87')[['Day', 'Month', 'long','lat','level','sal','Stations']].head(10))
#sns.relplot(x='Year', y='temp', data=df_new2)


#sns.relplot(x="Year", y="temp", data=df_new2)
#g = sns.relplot(x="Year", y="temp", kind="line", data=df_new2)
#sns.relplot(x="Year", y="temp", kind="line", data=df_new2.query('level == 10'))

#plt.show()






import pandas as pd

df = pd.read_csv('C:/Users/Egor/Desktop/Oxigen_result/All_parameters_without_none(New).csv', delimiter=',')
#df['temp'] = df['temp'].fillna(-10)
#df = df.query(' sal < 10')
#print(df[['Year','Month','long','lat','temp','sal','level','Stations']])
#max_t = df.temp.max()
#min_t = df.temp.min()
#max_sal = df.sal.max()
#min_sal = df.sal.min()
max_lat = df.lat.max()
min_lat = df.lat.min()
max_long = df.long.max()
min_long = df.long.min()
#print(min_lat,max_lat,min_long,max_long )

#df_level = df['level'].value_counts()
#print(df_level.head(20)

df_work = df.query('Year == 1978 & Month == 6')
df_last = df.query('Year == 1978 & Month == 6 & Day == 1')
for day in range(2,32):
    if day in list(df_work['Day']):
        df_new = df_work.query('Day == @day')
        df_new = df_new.drop_duplicates(['long','lat','level'])
        df_last = pd.concat([df_last, df_new])

df_without_dubl_month = df_last.drop_duplicates()

print(df_work.describe())
print(df_last.describe())
print(df_without_dubl_month.describe())


#print(df.query('sal >= 36')[['temp','sal','level','Stations','lat','long']])
#print(df.sal.max())
#print(df.sal.describe())

# ДЛЯ УДАЛЕНИЯ ДУБЛИКАТОВ В КАЖДОМ ДНЕ
#df1 = df.drop_duplicates(['long','lat','level'])
#print(df.describe())
#print(df1.describe())
#df = df.unique()


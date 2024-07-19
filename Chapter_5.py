import pandas as pd
df_crashes = pd.read_csv("Traffic_Crashes_-_Crashes_20240719.csv")
print(df_crashes.head())
print(df_crashes.info())
print(df_crashes.isnull().sum())
print(df_crashes.dropna(axis='columns', how='all', inplace=False))
print(df_crashes['REPORT_TYPE'].unique())
print(df_crashes.fillna(value={'REPORT_TYPE': 'ON SCENE'}))
#The total number of passenger cars involved in the crash can be found using the following code:
print(df_crashes.groupby('FIRST_CRASH_TYPE').agg({'CRASH_RECORD_ID': 'count'}).reset_index())

# renaming
col_rename={'CRASH_HOUR':'CRASH_HOURS'}
df_crashes=df_crashes.rename(columns=col_rename)
print(df_crashes.columns)
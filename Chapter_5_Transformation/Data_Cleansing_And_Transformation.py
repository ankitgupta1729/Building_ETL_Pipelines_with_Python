# Import modules
import pandas as pd
import logging

# define paths to data files
crash_data_file = "traffic_crashes.csv"
vehicle_crash_data_file = "traffic_crash_vehicle.csv"

# import data as dataframes
df_crashes = pd.read_csv(f"data/{crash_data_file}")
df_vehicles= pd.read_csv(f"data/{vehicle_crash_data_file}")

### Preliminary Tasks: The Importance of Staging Data

print(df_crashes.head())
print(df_crashes.info())
print(df_crashes.isnull().sum())
print(df_crashes.dropna(axis='columns', how='all', inplace=True) )
print(df_crashes.dropna(axis='index', thresh=2, inplace=False) )

##### Working with Missing Data

print(df_crashes['report_type'].unique())
# Let’s fill the missing value with ‘ON SCENE’ as below -
df_crashes  = df_crashes.fillna(value={'report_type': 'ON SCENE'})

#### Merging Data

# Merge crashes and vehicles dataframes
df = df_crashes.merge(df_vehicles, how = 'left',on='crash_record_id',suffixes=('_left', '_right'))
print(df.shape)

print(df.head())
df_agg = df.groupby('vehicle_type').agg({'crash_record_id': 'count'}).reset_index()
print(df_agg)

number_of_passenger_cars_involved = df_agg[df_agg['vehicle_type'] == 'PASSENGER']['crash_record_id'].array[0]
print(number_of_passenger_cars_involved)

#### Data Mapping with Target Data

# rename columns for data output
vehicle_mapping = {'vehicle_type':'vehicletypes'}
df_agg = df_agg.rename(columns=vehicle_mapping)
print(df_agg)

#####################################################################################

### Writing Transformation Functions

def get_transformed_data(crash_file, vehicle_file):
    # import data
    df_crashes = pd.read_csv(f"data/{crash_file}")
    df_vehicles = pd.read_csv(f"data/{vehicle_file}")

    # remove specified missing values
    under_threshold_removed = df_crashes.dropna(axis='index', thresh=2, inplace=False)
    under_threshold_rows = df_crashes[~df_crashes.index.isin(under_threshold_removed.index)]
    df_crashes.fillna(value={'report_type': 'ON SCENE'}, inplace=True)

    # merge crashes and vehicles
    df = df_crashes.merge(df_vehicles, how='left', on='crash_record_id', suffixes=('_left', '_right'))
    df_agg = df.groupby('vehicle_type').agg({'crash_record_id': 'count'}).reset_index()

    # transform column names for output data
    vehicle_mapping = {'vehicle_type': 'vehicletypes'}
    df_agg = df_agg.rename(columns=vehicle_mapping)

    return df_agg

get_transformed_data(crash_data_file,vehicle_crash_data_file)


###############################################################################

### Running the Workflow

#### The preceding code can be split into reusable functions that are easy to manage

# Read data from data source
def read_datasources(source_name):
    df = pd.read_csv(f"data/{source_name}")
    return df

# Drop rows with null values
def drop_rows_with_null_values(df):
    under_threshold_removed = df.dropna(axis='index', thresh=2, inplace=False)
    df = df[~df.index.isin(under_threshold_removed.index)]
    return df

# Fill missing values
def fill_missing_values(df):
    df = df.fillna(value={'report_type': 'ON SCENE'})
    return df

# Merge Dataframes
def merge_dataframes(df_vehicles,df_crashes):
    df = df_crashes.merge(df_vehicles,how='left', on='crash_record_id', suffixes=('_left', '_right'))
    return df

# Rename Columns
def rename_columns(df):
    vehicle_mapping = {'vehicle_type' :  'vehicletypes'}
    df = df.rename(columns=vehicle_mapping)
    return df

######################################################################################

#### Define the Pipeline Functions to run the Cleansing and Transformation Functions

def read_data_pipeline(crash_file, vehicle_file):
    df_crash = pd.DataFrame()
    df_vehicle_crash = pd.DataFrame()
    try:
        df_crash = read_datasources(crash_file)
        df_vehicle = read_datasources(vehicle_file)
    except Exception as e:
        logging.info("Exception in reading data pipeline")
    finally:
        return df_crash, df_vehicle


def drop_rows_with_null_values_pipeline(df_crash, df_vehicle):
    try:
        df_crash = drop_rows_with_null_values(df_crash)
        df_vehicle = drop_rows_with_null_values(df_vehicle)
    except Exception as e:
        logging.info("Exception in dropping rows with null value data pipeline")

    finally:
        return df_crash, df_vehicle


def fill_missing_values_pipeline(df_crash, df_vehicle):
    try:
        df_crash = fill_missing_values(df_crash)
        df_vehicle_crash = fill_missing_values(df_vehicle)
    except Exception as e:
        logging.info("Exception in filling missing value pipeline")

    finally:
        return df_crash, df_vehicle


def merge_dataframes_pipeline(df_crash, df_vehicle):
    try:
        df_agg = merge_dataframes(df_vehicles, df_crashes)
    except Exception as e:
        logging.info("Exception in merge dataframes pipeline")

    finally:
        return df_agg


def format_dataframes_pipeline(df_agg):
    try:
        df_output = rename_columns(df_agg)
    except Exception as e:
        logging.info("Exception in renaming dataframe columns pipeline")

    finally:
        return df_output

#### Use the Chigaco Traffic Data and Run the Pipeline Workflow

# Define input data
crash_data_file = "traffic_crashes.csv"
vehicle_crash_data_file = "traffic_crash_vehicle.csv"

# Read Data Pipeline
df_crash, df_vehicle = read_data_pipeline("traffic_crashes.csv", "traffic_crash_vehicle.csv")

# Drop Nulls
df_crash, df_vehicle = drop_rows_with_null_values_pipeline(df_crash, df_vehicle)

# Fill in Missing Values
df_crash, df_vehicle = fill_missing_values_pipeline(df_crash, df_vehicle)

# Merge Dataframes
df_agg = merge_dataframes_pipeline(df_crash, df_vehicle)

# Merge Dataframes
df_output = format_dataframes_pipeline(df_agg)

###################################################################################

### Transformation Activities in Python

READING_CRASH_DATA_PIPELINE = "<NOT_EXECUTED>"
DROPPING_ROW_WITH_NULL_PIPELINE = "<NOT_EXECUTED>"
FILLING_MISSING_VALUE_PIPELINE = "<NOT_EXECUTED>"
MERGE_DATAFRAME_PIPELINE = "<NOT_EXECUTED>"

df_crash, df_vehicle = read_data_pipeline("traffic_crashes.csv", "traffic_crash_vehicle.csv")

if READING_CRASH_DATA_PIPELINE == "<OK>":
    df_crash, df_vehicle = drop_rows_with_null_values_pipeline(df_crash, df_vehicle)

elif DROPPING_ROW_WITH_NULL_PIPELINE == "<OK>":
    df_crash, df_vehicle = fill_missing_values_pipeline(df_crash, df_vehicle)

elif FILLING_MISSING_VALUE_PIPELINE == "<OK>":
    df_crash, df_vehicle = merge_dataframes_pipeline(df_crash, df_vehicle_crash)
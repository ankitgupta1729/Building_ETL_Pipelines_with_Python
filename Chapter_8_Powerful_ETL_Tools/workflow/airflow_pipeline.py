
# https://stackoverflow.com/questions/67090596/airflow-pythonoperator-required-termios-module-on-window-10
# Import Modules
import yaml
from datetime import (datetime,timedelta)
from etl.extract import extract_data
from etl.transform import (transform_crash_data,transform_vehicle_data,transform_people_data)
#from etl.load import load_data
from airflow import DAG
from airflow.operators.python import PythonOperator


# import pipeline configuration
with open('../config.yaml', 'r') as file:
    config_data = yaml.safe_load(file)

# Define the DAG
default_args = {
    'owner': 'first_airflow_pipeline',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 19),
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
}
dag = DAG('chicago_dmv', default_args=default_args, schedule_interval=timedelta(days=1))

# Define the tasks
task_extract_crashes = PythonOperator(
    task_id='extract_crashes',
    op_kwargs={'filepath': config_data['crash_filepath'],
               'select_cols': config_data['crash_columns_list'],
               'rename_cols': config_data['crash_columns_rename_dict']},
    dag=dag
)
task_extract_vehicles = PythonOperator(
    task_id='extract_vehicles',
    python_callable=extract_data,
    op_kwargs={'filepath': config_data['vehicle_filepath'],
               'select_cols': config_data['vehicle_columns_list'],
               'rename_cols': config_data['vehicle_columns_rename_dict']},
    dag=dag
)
task_extract_people = PythonOperator(
    task_id='extract_people',
    python_callable=extract_data,
    op_kwargs={'filepath': config_data['people_filepath'],
               'select_cols': config_data['people_columns_list'],
               'rename_cols': config_data['people_columns_rename_dict']},
    dag=dag
)
task_transform_crashes = PythonOperator(
    task_id='transform_crashes',
    python_callable=transform_crash_data,
    op_kwargs={'crash_df': "{{ task_instance.xcom_pull(task_ids='extract_crashes') }}"},
    dag=dag
)
task_transform_vehicles = PythonOperator(
    task_id='transform_vehicles',
    python_callable=transform_vehicle_data,
    op_kwargs={'vehicle_df': "{{ task_instance.xcom_pull(task_ids='extract_vehicles') }}"},
    dag=dag
)
task_transform_people = PythonOperator(
    task_id='transform_people',
    python_callable=transform_people_data,
    op_kwargs={'people_df': "{{ task_instance.xcom_pull(task_ids='extract_people') }}"},
    dag=dag
)
# task_load_crash = PythonOperator(
#     task_id='load_crash',
#     python_callable=load_data,
#     op_kwargs={'df': "{{ task_instance.xcom_pull(task_ids='transform_crash') }}",
#                'create_PSQL': config_data['crash_create_PSQL'],
#                'insert_PSQL': config_data['crash_insert_PSQL']},
#     dag=dag
# )
# task_load_vehicle = PythonOperator(
#     task_id='load_vehicle',
#     python_callable=load_data,
#     op_kwargs={'df': "{{ task_instance.xcom_pull(task_ids='transform_vehicle') }}",
#                'create_PSQL': config_data['vehicle_create_PSQL'],
#                'insert_PSQL': config_data['vehicle_insert_PSQL']},
#     dag=dag
# )
# task_load_people = PythonOperator(
#     task_id='load_people',
#     python_callable=load_data,
#     op_kwargs={'df': "{{ task_instance.xcom_pull(task_ids='transform_people') }}",
#                'create_PSQL': config_data['crash_create_PSQL'],
#                'insert_PSQL': config_data['crash_insert_PSQL']},
#     dag=dag
# )


# Define the task dependencies
task_extract_crashes >> task_transform_crashes
task_extract_vehicles >> task_transform_vehicles
task_extract_people >> task_transform_people
# task_transform_crashes >> task_load_crash
# task_transform_vehicles >> task_load_vehicle
# task_transform_people >> task_load_people

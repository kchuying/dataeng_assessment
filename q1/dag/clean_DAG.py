from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.operators.email_operator import EmailOperator
from airflow.contrib.sensors.file_sensor import FileSensor

from datacleaner import data_cleaner

#Set varialbe yesterday_date
yesterday_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
# seven_days_ago = datetime.combine(datetime.today() - timedelta(7),
#                                       datetime.min.time())

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 12, 15, 1, 0),  #2021-12-15 01:00
    'email': ['kchuying@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=5), #can change to minutes
}

#Create DAG (workflow) -- syntax: dag id, default_args)
#schedule_interval: DAG will run every day, week, month etc.
#catchup = TRUE means it will run historical data for period specified
#template_searchpath is the directory for mounted SQL Script folder in A/F

#using context manager to automatically assign new operators to DAG (python keyword WITH)
with DAG('clean_file_dag',default_args=default_args,schedule_interval='@daily', template_searchpath=['/usr/local/airflow/sql_files'], catchup=True) as dag:
#alternatively, create variable dag = DAG(...), then you need to pass variable in each operator parameters
#dag=dag parameter will assign operator to DAG

    t1 = FileSensor(
        task_id='check_file1_exists',
        filepath='/usr/local/airflow/store_files_airflow/dataset1.csv',
        fs_conn_id='fs_default',
        poke_interval=10,
        timeout=150,
        soft_fail=True
    )

    t2 = FileSensor(
        task_id='check_file2_exists',
        filepath='/usr/local/airflow/store_files_airflow/dataset2.csv',
        fs_conn_id='fs_default',
        poke_interval=10,
        timeout=150,
        soft_fail=True
    )

    t3 = PythonOperator(task_id='clean_raw_csv', python_callable=data_cleaner)

    t4 = BashOperator(task_id='move_result_file', bash_command='cat ~/store_files_airflow/cleansed_data.csv && mv ~/store_files_airflow/cleansed_data.csv ~/store_files_airflow/results/cleansed_data_%s.csv' % yesterday_date)

#Send email to client, can add cc and bcc parameters
    t5 = EmailOperator(task_id='send_email_result',
        to='kchuying@gmail.com',
        subject='Daily report generated',
        html_content=""" <h1>Dataset is cleansed and ready for viewing.</h1> """,
        files=['/usr/local/airflow/store_files_airflow/results/cleansed_data_%s.csv' % yesterday_date])

    t6 = BashOperator(task_id='rename_raw_file1', bash_command='cat ~/store_files_airflow/dataset1.csv && mv ~/store_files_airflow/dataset1.csv ~/store_files_airflow/processed_files/dataset1_%s.csv' % yesterday_date)
    t7 = BashOperator(task_id='rename_raw_file2', bash_command='cat ~/store_files_airflow/dataset2.csv && mv ~/store_files_airflow/dataset2.csv ~/store_files_airflow/processed_files/dataset2_%s.csv' % yesterday_date)

# Run task in sequence
    [t1,t2] >> t3 >> t4 >> t5 >> [t6,t7]

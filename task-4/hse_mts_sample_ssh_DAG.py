from datetime import timedelta, datetime
import airflow
from airflow import DAG
from airflow.contrib.operators.ssh_operator import SSHOperator

default_args = {
            'owner': 'airflow',
            'depends_on_past': False,
            'email': ['airflow@example.com'],
            'email_on_failure': False,
            'email_on_retry': False,
            'start_date': '2023-12-05',
            'retries': 1,
            'retry_delay': timedelta(minutes=6000),
            'catchup': False
}

dag = DAG(dag_id='testing_stuff',
          default_args=default_args,
          schedule_interval='50 * * * *',
          dagrun_timeout=timedelta(seconds=600))

t1_bash = """
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=FILEID' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=FILEID" -O FILENAME && rm -rf /tmp/cookies.txt
""" # download file from google drive

t2_bash = ":" # do nothing, the file is already unzipped

t3_bash = """export PATH="" && hdfs dfs -put ./price_paid_records.csv /mydata""" # add file to hdfs

t4_bash = "hadoop jar hadoop-3.2.3/share/hadoop/tools/lib/hadoop-streaming-3.2.3.jar -files ./map.py,./reduce.py -mapper map.py -reducer reduce.py -input /mydata/price_paid_records.csv -output /mydata/output"

t5_bash = "hdfs dfs -cat /mydata/output/part-00000" # print result of MapReduce
t6_bash = "rm price_paid_records.csv" # delete csv file
t7_bash = "hdfs dfs -rm -r /mydata/output" # delete output from hadoop

t1 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='get_dataset_from_web',
                 command=t1_bash,
                 cmd_timeout=600,
                 dag=dag)

t2 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='unpack_archive',
                 command=t2_bash,
                 dag=dag)

t3 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='load_to_hdfs',
                 command=t3_bash,
                 cmd_timeout=300,
                 dag=dag)

t4 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='run_MR_job',
                 command=t4_bash,
                 cmd_timeout=300,
                 dag=dag)

t5 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='print_result',
                 command=t5_bash,
                 dag=dag)

t6 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='delete_csv',
                 command=t6_bash,
                 dag=dag)

t7 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='delete_output',
                 command=t7_bash,
                 dag=dag)

t1 >> t2 >> t3 >> t4 >> t5 >> t6 >> t7

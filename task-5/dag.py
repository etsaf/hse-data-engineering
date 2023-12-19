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
            'start_date': '2023-12-19',
            'retries': 1,
            'retry_delay': timedelta(minutes=6000),
            'catchup': False
}

dag = DAG(dag_id='testing_stuff_with_spark',
          default_args=default_args,
          schedule_interval='50 * * * *',
          dagrun_timeout=timedelta(seconds=600))

HADOOP_BIN_PREFIX = "/home/hdoop/hadoop-3.2.3/bin/"
HADOOP_STREAMING_JAR = "hadoop-3.2.3/share/hadoop/tools/lib/hadoop-streaming-3.2.3.jar"

t1_bash = """
wget https://gist.githubusercontent.com/vlerdman/84e9a162bccb6ec4a31e2435ba480bf8/raw/fc7523f98365196e22b33c009650226612d9464a/sd.csv -O sd.csv && \
wget https://raw.githubusercontent.com/etsaf/hse-data-engineering/main/task-3/map.py -O map.py && \
wget https://raw.githubusercontent.com/etsaf/hse-data-engineering/main/task-3/reduce.py -O reduce.py && \
wget https://raw.githubusercontent.com/etsaf/hse-data-engineering/main/task-5/spark.py -O spark.py
""" # download file and map/reduce scripts

t2_bash = ":" # do nothing, the file is already unzipped

t3_bash = "{}hdfs dfs -put ./sd.csv /mydata".format(HADOOP_BIN_PREFIX) # add file to hdfs

t4_bash = "{}hadoop jar {} -files ./map.py,./reduce.py -mapper \"python3 map.py\" -reducer \"python3 reduce.py\" -input /mydata/sd.csv -output /mydata/output".format(HADOOP_BIN_PREFIX, HADOOP_STREAMING_JAR)

t5_bash = "{}hdfs dfs -cat /mydata/output/part-00000".format(HADOOP_BIN_PREFIX) # print result of MapReduce

t6_bash = "source $HOME/venv/bin/activate && python3 spark.py" # convert to json with spark
t7_bash = "{}hdfs dfs -ls /mydata/sd.json".format(HADOOP_BIN_PREFIX) # check saving file

t8_bash = "{}hdfs dfs -rm -r /mydata/sd.csv && rm sd.csv && rm map.py && rm reduce.py".format(HADOOP_BIN_PREFIX) # delete csv file
t9_bash = "{}hdfs dfs -rm -r /mydata/output && {}hdfs dfs -rm -r /mydata/sd.json".format(HADOOP_BIN_PREFIX, HADOOP_BIN_PREFIX) # delete output from hadoop

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
                 task_id='run_spark',
                 command=t6_bash,
                 dag=dag)

t7 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='ls_spark_results',
                 command=t7_bash,
                 dag=dag)

t8 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='delete_csv',
                 command=t8_bash,
                 dag=dag)

t9 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='delete_output',
                 command=t9_bash,
                 dag=dag)

t1 >> t2 >> t3 >> t4 >> t5 >> t6 >> t7 >> t8 >> t9

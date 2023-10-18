# Задание 3. MapReduce

## Датасет

Найден [датасет](https://www.kaggle.com/datasets/hm-land-registry/uk-housing-prices-paid/) более 1 ГБ с данными по недвижимости в Великобритании на Каггле

**Пример данных**
| Transaction unique identifier          | Price | Date of Transfer | Property Type | Old/New | Duration | Town/City  | District           | County             | PPDCategory Type |
|----------------------------------------|-------|------------------|---------------|---------|----------|------------|--------------------|--------------------|------------------|
| {81B82214-7FBC-4129-9F6B-4956B4A663AD} | 25000 | 18/08/1995 00:00 | T             | N       | F        | OLDHAM     | OLDHAM             | GREATER MANCHESTER | A                |
| {8046EC72-1466-42D6-A753-4956BF7CD8A2} | 42500 | 09/08/1995 00:00 | S             | N       | F        | GRAYS      | THURROCK           | THURROCK           | A                |
| {278D581A-5BF3-4FCE-AF62-4956D87691E6} | 45000 | 30/06/1995 00:00 | T             | N       | F        | HIGHBRIDGE | SEDGEMOOR          | SOMERSET           | A                |
| {1D861C06-A416-4865-973C-4956DB12CD12} | 43150 | 24/11/1995 00:00 | T             | N       | F        | BEDFORD    | NORTH BEDFORDSHIRE | BEDFORDSHIRE       | A                |

## MapReduce

Написаны простые map и reduce для поиска максимальной стоимости недвижимости

**Map**
```python
#!/usr/bin/env python
"""map.py"""
import sys

delimiter = ','
for line in sys.stdin:
    arr = line.split(delimiter)
    price = arr[1]
    print(price)
```

**Reduce**
```python
#!/usr/bin/env python
"""reduce.py"""

import sys
import math

max_price = -math.inf
for line in sys.stdin:
    price = int(line.strip())
    if price > max_price:
        max_price = price

print(max_price)
```

## Hadoop

Подключившись к виртуальной машине, добавляем `map.py` и `reduce.py`

```bash
nano map.py
nano reduce.py
```

Загружаем с гугл-диска `price_paid_records.csv`

```bash
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=FILEID' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=FILEID" -O FILENAME && rm -rf /tmp/cookies.txt

hdfs dfs -put ./price_paid_records.csv /mydata
```

При желании проверяем наличие файла
```bash
hdfs dfs -ls -R /mydata
```

### Без Hadoop

Запускаем MapReduce
```
$ /usr/bin/time -v cat price_paid_records.csv | ./map.py | ./reduce.py

Command being timed: "cat price_paid_records.csv"
	User time (seconds): 0.02
	System time (seconds): 1.90
	Percent of CPU this job got: 8%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:23.88
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 2020
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 0
	Minor (reclaiming a frame) page faults: 119
	Voluntary context switches: 291998
	Involuntary context switches: 203
	Swaps: 0
	File system inputs: 0
	File system outputs: 0
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
98900000
```

### Hadoop Cluster

Запускаем Hadoop Cluster
```bash
cd hadoop-3.2.3/sbin
./start-all.sh
cd ../..
```

Запускаем MapReduce на Hadoop Cluster
```bash
$ hadoop jar hadoop-3.2.3/share/hadoop/tools/lib/hadoop-streaming-3.2.3.jar -files ./map.py,./reduce.py -mapper map.py -reducer reduce.py -input /mydata/price_paid_records.csv -output /mydata/output

2023-10-18 14:39:50,345 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
packageJobJar: [/tmp/hadoop-unjar621648412996836061/] [] /tmp/streamjob980724060771352142.jar tmpDir=null
2023-10-18 14:39:50,961 INFO client.RMProxy: Connecting to ResourceManager at /127.0.0.1:8032
2023-10-18 14:39:51,131 INFO client.RMProxy: Connecting to ResourceManager at /127.0.0.1:8032
2023-10-18 14:39:51,321 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/hdoop/.staging/job_1697628422270_0008
2023-10-18 14:39:51,587 INFO mapred.FileInputFormat: Total input files to process : 1
2023-10-18 14:39:51,642 INFO mapreduce.JobSubmitter: number of splits:18
2023-10-18 14:39:51,762 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1697628422270_0008
2023-10-18 14:39:51,764 INFO mapreduce.JobSubmitter: Executing with tokens: []
2023-10-18 14:39:51,940 INFO conf.Configuration: resource-types.xml not found
2023-10-18 14:39:51,940 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
2023-10-18 14:39:52,025 INFO impl.YarnClientImpl: Submitted application application_1697628422270_0008
2023-10-18 14:39:52,054 INFO mapreduce.Job: The url to track the job: http://mts-hse-de-course-team-5-1.msk.internal:8088/proxy/application_1697628422270_0008/
2023-10-18 14:39:52,056 INFO mapreduce.Job: Running job: job_1697628422270_0008
2023-10-18 14:39:57,126 INFO mapreduce.Job: Job job_1697628422270_0008 running in uber mode : false
2023-10-18 14:39:57,127 INFO mapreduce.Job:  map 0% reduce 0%
2023-10-18 14:40:08,246 INFO mapreduce.Job:  map 6% reduce 0%
2023-10-18 14:40:10,266 INFO mapreduce.Job:  map 11% reduce 0%
2023-10-18 14:40:13,282 INFO mapreduce.Job:  map 22% reduce 0%
2023-10-18 14:40:15,297 INFO mapreduce.Job:  map 28% reduce 0%
2023-10-18 14:40:16,304 INFO mapreduce.Job:  map 33% reduce 0%
2023-10-18 14:40:23,546 INFO mapreduce.Job:  map 39% reduce 0%
2023-10-18 14:40:27,732 INFO mapreduce.Job:  map 44% reduce 0%
2023-10-18 14:40:28,738 INFO mapreduce.Job:  map 50% reduce 0%
2023-10-18 14:40:29,758 INFO mapreduce.Job:  map 56% reduce 0%
2023-10-18 14:40:33,793 INFO mapreduce.Job:  map 61% reduce 0%
2023-10-18 14:40:35,916 INFO mapreduce.Job:  map 61% reduce 20%
2023-10-18 14:40:36,952 INFO mapreduce.Job:  map 67% reduce 20%
2023-10-18 14:40:41,051 INFO mapreduce.Job:  map 67% reduce 22%
2023-10-18 14:40:42,055 INFO mapreduce.Job:  map 72% reduce 22%
2023-10-18 14:40:43,140 INFO mapreduce.Job:  map 78% reduce 22%
2023-10-18 14:40:44,146 INFO mapreduce.Job:  map 83% reduce 22%
2023-10-18 14:40:47,157 INFO mapreduce.Job:  map 89% reduce 28%
2023-10-18 14:40:49,164 INFO mapreduce.Job:  map 94% reduce 28%
2023-10-18 14:40:50,170 INFO mapreduce.Job:  map 100% reduce 28%
2023-10-18 14:40:53,181 INFO mapreduce.Job:  map 100% reduce 49%
2023-10-18 14:40:59,207 INFO mapreduce.Job:  map 100% reduce 76%
2023-10-18 14:41:05,239 INFO mapreduce.Job:  map 100% reduce 95%
2023-10-18 14:41:07,246 INFO mapreduce.Job:  map 100% reduce 100%
2023-10-18 14:41:07,251 INFO mapreduce.Job: Job job_1697628422270_0008 completed successfully
2023-10-18 14:41:07,323 INFO mapreduce.Job: Counters: 55
	File System Counters
		FILE: Number of bytes read=216717963
		FILE: Number of bytes written=437991896
		FILE: Number of read operations=0
		FILE: Number of large read operations=0
		FILE: Number of write operations=0
		HDFS: Number of bytes read=2405757298
		HDFS: Number of bytes written=10
		HDFS: Number of read operations=59
		HDFS: Number of large read operations=0
		HDFS: Number of write operations=2
		HDFS: Number of bytes read erasure-coded=0
	Job Counters 
		Killed map tasks=1
		Launched map tasks=18
		Launched reduce tasks=1
		Rack-local map tasks=18
		Total time spent by all maps in occupied slots (ms)=209065
		Total time spent by all reduces in occupied slots (ms)=49461
		Total time spent by all map tasks (ms)=209065
		Total time spent by all reduce tasks (ms)=49461
		Total vcore-milliseconds taken by all map tasks=209065
		Total vcore-milliseconds taken by all reduce tasks=49461
		Total megabyte-milliseconds taken by all map tasks=214082560
		Total megabyte-milliseconds taken by all reduce tasks=50648064
	Map-Reduce Framework
		Map input records=22489349
		Map output records=22489348
		Map output bytes=171739261
		Map output materialized bytes=216718065
		Input split bytes=1764
		Combine input records=0
		Combine output records=0
		Reduce input groups=172773
		Reduce shuffle bytes=216718065
		Reduce input records=22489348
		Reduce output records=1
		Spilled Records=44978696
		Shuffled Maps =18
		Failed Shuffles=0
		Merged Map outputs=18
		GC time elapsed (ms)=4207
		CPU time spent (ms)=97080
		Physical memory (bytes) snapshot=6904492032
		Virtual memory (bytes) snapshot=48279011328
		Total committed heap usage (bytes)=5982126080
		Peak Map Physical memory (bytes)=465690624
		Peak Map Virtual memory (bytes)=2547068928
		Peak Reduce Physical memory (bytes)=409096192
		Peak Reduce Virtual memory (bytes)=2560147456
	Shuffle Errors
		BAD_ID=0
		CONNECTION=0
		IO_ERROR=0
		WRONG_LENGTH=0
		WRONG_MAP=0
		WRONG_REDUCE=0
	File Input Format Counters 
		Bytes Read=2405755534
	File Output Format Counters 
		Bytes Written=10
2023-10-18 14:41:07,323 INFO streaming.StreamJob: Output directory: /mydata/output
```

Переносим результат MapReduce на локальную машину
```
hdfs dfs -get /mydata/output ./output
cd output/output
nano part-00000
```

Получили результат `98900000`, что сходится с мнением Kaggle - _98.9m Max_

Для удаления папки output из файловой системы Hadoop используем
```bash
hdfs dfs -rm -r /mydata/output
```

## Результаты

|                | Без Hadoop | Hadoop Standalone | Hadoop Cluster |
|----------------|------------|-------------------|----------------|
| Время, seconds |    24.52   |                   |     70,196     |
| Память, bytes  |   2020000  |                   |   465690624    |



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

Запускаем Hadoop Cluster
```bash
cd hadoop-3.2.3/sbin
./start-all.sh
cd ../..
```

Запускаем MapReduce на Hadoop Cluster
```bash
$ hadoop jar hadoop-3.2.3/share/hadoop/tools/lib/hadoop-streaming-3.2.3.jar -file ./map.py -mapper map.py \
-file ./reduce.py -reducer reduce.py \
-input /mydata/uk_property.csv -output /mydata/output

2023-10-18 11:29:00,616 INFO mapreduce.Job: Running job: job_1697628422270_0001
2023-10-18 11:29:06,729 INFO mapreduce.Job: Job job_1697628422270_0001 running in uber mode : false
2023-10-18 11:29:06,730 INFO mapreduce.Job:  map 0% reduce 0%
2023-10-18 11:29:11,804 INFO mapreduce.Job:  map 50% reduce 0%
2023-10-18 11:29:12,810 INFO mapreduce.Job:  map 100% reduce 0%
2023-10-18 11:29:16,835 INFO mapreduce.Job:  map 100% reduce 100%
2023-10-18 11:29:17,848 INFO mapreduce.Job: Job job_1697628422270_0001 completed successfully
2023-10-18 11:29:17,939 INFO mapreduce.Job: Counters: 54
	File System Counters
		FILE: Number of bytes read=42
		FILE: Number of bytes written=719324
		FILE: Number of read operations=0
		FILE: Number of large read operations=0
		FILE: Number of write operations=0
		HDFS: Number of bytes read=793
		HDFS: Number of bytes written=7
		HDFS: Number of read operations=11
		HDFS: Number of large read operations=0
		HDFS: Number of write operations=2
		HDFS: Number of bytes read erasure-coded=0
	Job Counters 
		Launched map tasks=2
		Launched reduce tasks=1
		Rack-local map tasks=2
		Total time spent by all maps in occupied slots (ms)=4063
		Total time spent by all reduces in occupied slots (ms)=2021
		Total time spent by all map tasks (ms)=4063
		Total time spent by all reduce tasks (ms)=2021
		Total vcore-milliseconds taken by all map tasks=4063
		Total vcore-milliseconds taken by all reduce tasks=2021
		Total megabyte-milliseconds taken by all map tasks=4160512
		Total megabyte-milliseconds taken by all reduce tasks=2069504
	Map-Reduce Framework
		Map input records=4
		Map output records=4
		Map output bytes=28
		Map output materialized bytes=48
		Input split bytes=182
		Combine input records=0
		Combine output records=0
		Reduce input groups=4
		Reduce shuffle bytes=48
		Reduce input records=4
		Reduce output records=1
		Spilled Records=8
		Shuffled Maps =2
		Failed Shuffles=0
		Merged Map outputs=2
		GC time elapsed (ms)=147
		CPU time spent (ms)=1680
		Physical memory (bytes) snapshot=906395648
		Virtual memory (bytes) snapshot=7634395136
		Total committed heap usage (bytes)=799539200
		Peak Map Physical memory (bytes)=334667776
		Peak Map Virtual memory (bytes)=2545418240
		Peak Reduce Physical memory (bytes)=245329920
		Peak Reduce Virtual memory (bytes)=2550865920
	Shuffle Errors
		BAD_ID=0
		CONNECTION=0
		IO_ERROR=0
		WRONG_LENGTH=0
		WRONG_MAP=0
		WRONG_REDUCE=0
	File Input Format Counters 
		Bytes Read=611
	File Output Format Counters 
		Bytes Written=7
2023-10-18 11:29:17,940 INFO streaming.StreamJob: Output directory: /mydata/output
```

## Результаты

|               | Без Hadoop | Hadoop Standalone | Hadoop Cluster |
|---------------|------------|-------------------|----------------|
| Время, ms     |            |                   |                |
| Память, bytes |            |                   |                |



# Задание 1. Hadoop

### Установка hadoop кластера из одной ноды

```shell
sudo apt install openjdk-8-jdk -y
sudo adduser hdoop
su - hdoop
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys
ssh localhost
wget https://downloads.apache.org/hadoop/common/hadoop-3.2.3/hadoop-3.2.3.tar.gz
tar xzf hadoop-3.2.3.tar.gz
```

```shell
sudo nano .bashrc
#Copy the following Hadoop Related Options
export HADOOP_HOME=/home/hdoop/hadoop-3.2.3
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/nativ"

source ~/.bashrc
```



```shell
sudo nano $HADOOP_HOME/etc/hadoop/hadoop-env.sh
#Uncomment the $JAVA_HOME variable and add the full path to the OpenJDK installation on your system
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
```
```shell
sudo nano $HADOOP_HOME/etc/hadoop/core-site.xml
 
#Copy the following to the file 
<configuration>
<property>
<name>hadoop.tmp.dir</name>
<value>/home/hdoop/tmpdata</value>
</property>
<property>
<name>fs.default.name</name>
<value>hdfs://127.0.0.1:9000</value>
</property>
</configuration>
```

```shell
sudo nano $HADOOP_HOME/etc/hadoop/hdfs-site.xml
 
#Add the following configuration to the file and, if needed, adjust the NameNode and DataNode directories to your custom locations.
<configuration>
<property>
<name>dfs.data.dir</name>
<value>/home/hdoop/dfsdata/namenode</value>
</property>
<property>
<name>dfs.data.dir</name>
<value>/home/hdoop/dfsdata/datanode</value>
</property>
<property>
<name>dfs.replication</name>
<value>1</value>
</property>
</configuration>
```

```shell
mkdir /home/hdoop/tmpdata
mkdir /home/hdoop/dfsdata/namenode
mkdir /home/hdoop/dfsdata/datanode

hdfs namenode -format
cd hadoop-3.2.3/sbin
./start-dfs.sh
```

### Добавляем файл

```shell
wget https://gist.githubusercontent.com/khaykov/a6105154becce4c0530da38e723c2330/raw/41ab415ac41c93a198f7da5b47d604956157c5c3/gistfile1.txt
hdfs dfs -mkdir /data
hdfs dfs -put gistfile1.txt /data
```

```shell
hdfs dfs -du -h /data
1.0 M  1.0 M  /data/gistfile1.txt
```

```shell
du -ah ./dfsdata
4.0K	./dfsdata/namenode
4.0K	./dfsdata/datanode/in_use.lock
4.0K	./dfsdata/datanode/current/BP-2145698090-127.0.1.1-1696440288143/tmp
4.0K	./dfsdata/datanode/current/BP-2145698090-127.0.1.1-1696440288143/scanner.cursor
1.0M	./dfsdata/datanode/current/BP-2145698090-127.0.1.1-1696440288143/current/finalized/subdir0/subdir0/blk_1073741827
12K	./dfsdata/datanode/current/BP-2145698090-127.0.1.1-1696440288143/current/finalized/subdir0/subdir0/blk_1073741827_1003.meta
1.1M	./dfsdata/datanode/current/BP-2145698090-127.0.1.1-1696440288143/current/finalized/subdir0/subdir0
1.1M	./dfsdata/datanode/current/BP-2145698090-127.0.1.1-1696440288143/current/finalized/subdir0
1.1M	./dfsdata/datanode/current/BP-2145698090-127.0.1.1-1696440288143/current/finalized
4.0K	./dfsdata/datanode/current/BP-2145698090-127.0.1.1-1696440288143/current/dfsUsed
4.0K	./dfsdata/datanode/current/BP-2145698090-127.0.1.1-1696440288143/current/rbw
4.0K	./dfsdata/datanode/current/BP-2145698090-127.0.1.1-1696440288143/current/VERSION
1.1M	./dfsdata/datanode/current/BP-2145698090-127.0.1.1-1696440288143/current
1.1M	./dfsdata/datanode/current/BP-2145698090-127.0.1.1-1696440288143
4.0K	./dfsdata/datanode/current/VERSION
1.1M	./dfsdata/datanode/current
1.1M	./dfsdata/datanode
1.1M	./dfsdata
```

### Расширяем hadoop кластер до 3 нод

```shell
sudo nano /etc/hosts

10.0.10.7  main
10.0.10.15 slave1
10.0.10.16 slave2
```

```shell
scp .ssh/id_rsa.pub hdoop@slave1:/home/hdoop/.ssh/authorized_keys
scp .ssh/id_rsa.pub hdoop@slave2:/home/hdoop/.ssh/authorized_keys
```

```shell
sudo nano $HADOOP_HOME/etc/hadoop/workers

main
slave1
slave2
```

```shell
sudo nano $HADOOP_HOME/etc/hadoop/hdfs-site.xml
 
#Add the following configuration to the file and, if needed, adjust the NameNode and DataNode directories to your custom locations.
<configuration>
<property>
<name>dfs.data.dir</name>
<value>/home/hdoop/dfsdata/namenode</value>
</property>
<property>
<name>dfs.data.dir</name>
<value>/home/hdoop/dfsdata/datanode</value>
</property>
<property>
<name>dfs.replication</name>
<value>3</value>
</property>
</configuration>
```

```shell
sudo nano $HADOOP_HOME/etc/hadoop/core-site.xml
 
#Copy the following to the file 
<configuration>
<property>
<name>hadoop.tmp.dir</name>
<value>/home/hdoop/tmpdata</value>
</property>
<property>
<name>fs.default.name</name>
<value>hdfs://main:9000</value>
</property>
</configuration>
```

```shell
hdfs dfs -du -h /data
1.0 M  3.0 M  /data/gistfile1.txt
```

```shell
du -ah ./dfsdata
4.0K	./dfsdata/namenode
4.0K	./dfsdata/datanode/current/BP-2145698090-127.0.1.1-1696440288143/tmp
4.0K	./dfsdata/datanode/current/BP-2145698090-127.0.1.1-1696440288143/scanner.cursor
1.0M	./dfsdata/datanode/current/BP-2145698090-127.0.1.1-1696440288143/current/finalized/subdir0/subdir0/blk_1073741827
12K	./dfsdata/datanode/current/BP-2145698090-127.0.1.1-1696440288143/current/finalized/subdir0/subdir0/blk_1073741827_1003.meta
1.1M	./dfsdata/datanode/current/BP-2145698090-127.0.1.1-1696440288143/current/finalized/subdir0/subdir0
1.1M	./dfsdata/datanode/current/BP-2145698090-127.0.1.1-1696440288143/current/finalized/subdir0
1.1M	./dfsdata/datanode/current/BP-2145698090-127.0.1.1-1696440288143/current/finalized
4.0K	./dfsdata/datanode/current/BP-2145698090-127.0.1.1-1696440288143/current/dfsUsed
4.0K	./dfsdata/datanode/current/BP-2145698090-127.0.1.1-1696440288143/current/rbw
4.0K	./dfsdata/datanode/current/BP-2145698090-127.0.1.1-1696440288143/current/VERSION
1.1M	./dfsdata/datanode/current/BP-2145698090-127.0.1.1-1696440288143/current
1.1M	./dfsdata/datanode/current/BP-2145698090-127.0.1.1-1696440288143
4.0K	./dfsdata/datanode/current/VERSION
1.1M	./dfsdata/datanode/current
1.1M	./dfsdata/datanode
1.1M	./dfsdata
```

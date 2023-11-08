# Задание 2. Ресурсы, журнал изменений


## 1 большой файл

```
    openssl rand 1100000000 >bigfile.txt    # создаем файл ~1.1Gb с рандомными байтами

    -rw-rw-r--  1 hdoop hdoop 1.1G Oct 20 12:05  bigfile.txt
```

#### До загрузки

```
df -h /

Filesystem      Size  Used Avail Use% Mounted on
/dev/sda2       295G   13G  270G   5% /

Filesystem      Size  Used Avail Use% Mounted on
/dev/sda2       295G   11G  272G   4% /

Filesystem      Size  Used Avail Use% Mounted on
/dev/sda2       295G   11G  272G   4% /
```

```
ls -lah ./tmpdata/dfs/namesecondary/current/ | tail

-rw-rw-r-- 1 hdoop hdoop   42 Oct 11 11:56 edits_0000000000000000216-0000000000000000217
-rw-rw-r-- 1 hdoop hdoop   42 Oct 11 12:56 edits_0000000000000000218-0000000000000000219
-rw-rw-r-- 1 hdoop hdoop   42 Oct 11 13:56 edits_0000000000000000220-0000000000000000221
-rw-rw-r-- 1 hdoop hdoop   42 Oct 11 14:56 edits_0000000000000000222-0000000000000000223
-rw-rw-r-- 1 hdoop hdoop  114 Oct 11 15:56 edits_0000000000000000224-0000000000000000226
-rw-rw-r-- 1 hdoop hdoop  578 Oct 11 14:56 fsimage_0000000000000000223
-rw-rw-r-- 1 hdoop hdoop   62 Oct 11 14:56 fsimage_0000000000000000223.md5
-rw-rw-r-- 1 hdoop hdoop  634 Oct 11 15:56 fsimage_0000000000000000226
-rw-rw-r-- 1 hdoop hdoop   62 Oct 11 15:56 fsimage_0000000000000000226.md5
-rw-rw-r-- 1 hdoop hdoop  214 Oct 11 15:56 VERSION
```

```
hdfs oiv -p FileDistribution -i ./tmpdata/dfs/namesecondary/current/fsimage_0000000000000000226

Processed 0 inodes.
Size	NumFiles
2097152	2
totalFiles = 2
totalDirectories = 2
totalBlocks = 2
totalSpace = 2097150
maxFileSize = 1048575
```

```
hdfs oev -p xml -i ./tmpdata/dfs/namesecondary/current/edits_0000000000000000224-0000000000000000226 -o edits_log.xml && cat edits_log.xml

<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<EDITS>
  <EDITS_VERSION>-65</EDITS_VERSION>
  <RECORD>
    <OPCODE>OP_START_LOG_SEGMENT</OPCODE>
    <DATA>
      <TXID>224</TXID>
    </DATA>
  </RECORD>
  <RECORD>
    <OPCODE>OP_MKDIR</OPCODE>
    <DATA>
      <TXID>225</TXID>
      <LENGTH>0</LENGTH>
      <INODEID>16388</INODEID>
      <PATH>/data</PATH>
      <TIMESTAMP>1697039664783</TIMESTAMP>
      <PERMISSION_STATUS>
        <USERNAME>hdoop</USERNAME>
        <GROUPNAME>supergroup</GROUPNAME>
        <MODE>493</MODE>
      </PERMISSION_STATUS>
    </DATA>
  </RECORD>
  <RECORD>
    <OPCODE>OP_END_LOG_SEGMENT</OPCODE>
    <DATA>
      <TXID>226</TXID>
    </DATA>
  </RECORD>
</EDITS>
```

#### Загружаем файл в hdfs

```
hdfs dfs -put ./bigfile.txt /bigfiles
```


#### После загрузки

```
df -h /

Filesystem      Size  Used Avail Use% Mounted on
/dev/sda2       295G   13G  270G   5% /

Filesystem      Size  Used Avail Use% Mounted on
/dev/sda2       295G   12G  271G   5% /

Filesystem      Size  Used Avail Use% Mounted on
/dev/sda2       295G   12G  271G   5% /
```

```
```


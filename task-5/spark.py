import pyspark 
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
import pyspark.sql.types as tp

spark = SparkSession.builder.master("local").appName("hdfs_test").getOrCreate()

booksSchema = StructType().add("id", "integer").add("price", tp.LongType()).add("room_id", "integer").add("street_id", "integer")
booksdata=spark.read.csv("hdfs://main:9000/mydata/sd.csv", schema=booksSchema)
booksdata.show(5)
booksdata.printSchema()
booksdata.write.json("hdfs://main:9000/mydata/sd.json")

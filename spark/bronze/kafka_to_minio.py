from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

# 1. Buat Spark Session
spark = SparkSession.builder \
    .appName("KafkaToMinIO") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# 2. Schema data (sesuai CSV kamu)
schema = StructType([
    StructField("Book", StringType(), True),
    StructField("Author(s)", StringType(), True),
    StructField("Original language", StringType(), True),
    StructField("First published", IntegerType(), True),
    StructField("Approximate sales in millions", DoubleType(), True),
    StructField("Genre", StringType(), True),
])

# 3. Baca stream dari Kafka
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "sensor_stream") \
    .option("startingOffsets", "earliest") \
    .load()

# 4. Parse JSON
value_df = kafka_df.selectExpr("CAST(value AS STRING) as json_str")

parsed_df = value_df.select(
    from_json(col("json_str"), schema).alias("data")
).select("data.*")

# 5. Tulis ke MinIO (raw zone)
query = parsed_df.writeStream \
    .format("parquet") \
    .option("path", "s3a://raw/books") \
    .option("checkpointLocation", "s3a://raw/checkpoints/books") \
    .outputMode("append") \
    .start()

query.awaitTermination()

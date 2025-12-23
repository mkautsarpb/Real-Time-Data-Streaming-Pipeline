from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MinIOToPostgres") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# --- Konfigurasi MinIO (S3A) ---
hadoop_conf = spark._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3a.endpoint", "http://minio:9000")
hadoop_conf.set("fs.s3a.access.key", "minio")
hadoop_conf.set("fs.s3a.secret.key", "minio123")
hadoop_conf.set("fs.s3a.path.style.access", "true")
hadoop_conf.set("fs.s3a.connection.ssl.enabled", "false")

# --- Read from MinIO ---
df = spark.read.parquet("s3a://raw/books")

print("Jumlah data:", df.count())

# --- Write to PostgreSQL ---
df.write \
  .format("jdbc") \
  .option("url", "jdbc:postgresql://postgres:5432/de_db") \
  .option("dbtable", "books_raw") \
  .option("user", "de_user") \
  .option("password", "de_pass") \
  .option("driver", "org.postgresql.Driver") \
  .mode("overwrite") \
  .save()

print("✅ Data berhasil ditulis ke PostgreSQL (books_raw)")

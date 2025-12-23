from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp

spark = SparkSession.builder \
    .appName("RawToSilverBooks") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# =====================
# READ RAW DATA
# =====================
raw_path = "s3a://raw/books"

raw_df = spark.read.parquet(raw_path)

# =====================
# TRANSFORM → SILVER
# =====================
silver_df = (
    raw_df
    .withColumnRenamed("Book", "book_title")
    .withColumnRenamed("Author(s)", "authors")
    .withColumnRenamed("Original language", "original_language")
    .withColumnRenamed("First published", "first_published_year")
    .withColumnRenamed("Approximate sales in millions", "sales_millions")
    .withColumnRenamed("Genre", "genre")
    .withColumn("first_published_year", col("first_published_year").cast("int"))
    .withColumn("sales_millions", col("sales_millions").cast("double"))
    .withColumn("ingested_at", current_timestamp())
    .filter(col("book_title").isNotNull())
)

# =====================
# WRITE SILVER DATA
# =====================
silver_path = "s3a://processed/books"

silver_df.write \
    .mode("overwrite") \
    .parquet(silver_path)

print("✅ Silver layer books written successfully")

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("SilverToPostgresBooks") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# =====================
# READ SILVER DATA
# =====================
silver_path = "s3a://processed/books"

df = spark.read.parquet(silver_path)

# =====================
# POSTGRES CONFIG
# =====================
jdbc_url = "jdbc:postgresql://postgres:5432/de_db"

connection_properties = {
    "user": "de_user",
    "password": "de_pass",
    "driver": "org.postgresql.Driver"
}

# =====================
# WRITE TO POSTGRES
# =====================
df.write \
    .mode("overwrite") \
    .jdbc(
        url=jdbc_url,
        table="books_silver",
        properties=connection_properties
    )

print("✅ Data successfully loaded into PostgreSQL (books_silver)")

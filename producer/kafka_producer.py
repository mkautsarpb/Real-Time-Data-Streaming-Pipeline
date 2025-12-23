import json
import time
import pandas as pd
from kafka import KafkaProducer

# 1. Koneksi ke Kafka
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# 2. Baca CSVS
df = pd.read_csv("../data/best-selling-books.csv")

print("🚀 Mulai kirim data ke Kafka...")

# 3. Kirim baris satu per satu
for _, row in df.iterrows():
    message = row.to_dict()
    producer.send("sensor_stream", value=message)
    print("Sent:", message)
    time.sleep(0.5)  # biar keliatan streaming

producer.flush()
print("✅ Selesai.")

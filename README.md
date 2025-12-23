# Real-Time-Data-Streaming-Pipeline

## 📌 Project Overview
This project implements an **end-to-end real-time data engineering pipeline** using a modern data stack.
It simulates streaming data ingestion, processes it through a lakehouse architecture, and delivers
analytics-ready data for business intelligence.

The pipeline follows **industry best practices**, including:
- Streaming ingestion
- Medallion architecture (Bronze → Silver → Gold)
- Data warehouse modeling with dbt
- Data quality testing

---

## 🏗️ Architecture Overview

Python Producer
↓
Apache Kafka (sensor_stream topic)
↓
Spark Structured Streaming
↓
MinIO (Data Lake)
├── Raw (Bronze)
└── Processed (Silver)
↓
PostgreSQL (Data Warehouse)
↓
dbt (Gold Layer: Fact & Dimension)
↓
BI / Analytics (Superset-ready)


---

## 🎯 Project Objectives
- Simulate real-time streaming from a CSV dataset
- Ingest data using Apache Kafka
- Process streaming data with Spark Structured Streaming
- Store raw and curated data in an S3-compatible data lake
- Load analytics-ready data into PostgreSQL
- Apply data modeling and quality tests using dbt

---

## 🧰 Technology Stack

| Layer | Technology |
|------|-----------|
| Data Generator | Python |
| Message Broker | Apache Kafka |
| Stream Processing | Apache Spark Structured Streaming |
| Data Lake | MinIO (S3-compatible) |
| Data Warehouse | PostgreSQL |
| Analytics Engineering | dbt |
| Orchestration | Docker Compose |

---

## 📂 Project Structure

project-root/
├── docker-compose.yml
├── data/
│ └── best-selling-books.csv
├── producer/
│ └── kafka_producer.py
├── spark/
│ ├── streaming/
│ │ └── kafka_to_minio.py
│ ├── silver/
│ │ └── raw_to_silver_books.py
│ └── warehouse/
│ └── silver_to_postgres_books.py
├── books_analytics/
│ └── models/
│ ├── staging/
│ │ └── stg_books.sql
│ └── marts/
│ ├── dim_author.sql
│ └── fact_books.sql
└── README.md


---

## 🔄 Data Flow Explanation

### 1. Python Producer
Reads a CSV file and sends each row as a JSON message to Kafka with a configurable delay.

### 2. Kafka
Acts as the streaming backbone, storing real-time events in a Kafka topic.

### 3. Spark Structured Streaming (Bronze)
Consumes Kafka messages and writes raw streaming data to MinIO.

### 4. Spark Batch Processing (Silver)
Reads raw data, cleans and standardizes it, and writes curated data back to MinIO.

### 5. PostgreSQL Warehouse
Loads curated Silver data into relational tables for analytics.

### 6. dbt (Gold Layer)
Transforms warehouse data into:
- Staging models
- Fact tables
- Dimension tables  
Includes data quality and relationship tests.

---

## 🧪 Data Quality
Implemented using dbt:
- `not_null` tests
- `unique` tests
- `relationships` tests between fact and dimension tables

---

## 📈 Use Cases
- Real-time ingestion pipeline demonstration
- Analytics-ready warehouse modeling
- Foundation for BI dashboards and reporting
- Portfolio project for Data Engineering / Analytics Engineering roles

---

## 🚀 How to Run (High-Level)

```bash
docker compose up -d
python producer/kafka_producer.py
spark-submit spark/streaming/kafka_to_minio.py
spark-submit spark/silver/raw_to_silver_books.py
spark-submit spark/warehouse/silver_to_postgres_books.py
dbt run
dbt test

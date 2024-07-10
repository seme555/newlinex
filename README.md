# **NewlineX â€” Batch Data Pipeline with Airflow, DuckDB, Delta Lake, Trino and Metabase**

![Docker](https://img.shields.io/badge/Docker-Enabled-blue?logo=docker) ![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-Orchestration-017CEE?logo=apacheairflow) ![DuckDB](https://img.shields.io/badge/DuckDB-Processing-yellow?logo=duckdb) ![Delta Lake](https://img.shields.io/badge/Delta%20Lake-Table%20Format-blue?logo=delta) ![Trino](https://img.shields.io/badge/Trino-SQL%20Query%20Engine-green?logo=trino) ![Metabase](https://img.shields.io/badge/Metabase-Visualization-509EE3?logo=metabase)

---

## **ðŸ“– Overview**
This project demonstrates a **batch data pipeline** following the **Medallion Architecture** (Bronze â†’ Silver â†’ Gold). It showcases how to ingest, clean, validate, aggregate, and visualize sales data using modern data engineering tools, all containerized with Docker for easy deployment.

ðŸ”Ž **Technologies Used:**

- **Orchestration:** [Apache Airflow](https://airflow.apache.org/)
- **Data Processing:** [DuckDB](https://duckdb.org/)
- **Data Lake Format:** [Delta Lake](https://delta.io/)
- **Object Storage:** [MinIO (S3-compatible)](https://min.io/)
- **Query Engine:** [Trino](https://trino.io/)
- **Visualization:** [Metabase](https://www.metabase.com/)
- **Data Quality:** [Soda Core](https://www.soda.io/)
- **Lineage:** [OpenLineage](https://openlineage.io/) + [Marquez](https://marquezproject.ai/)
- **Observability:** [Prometheus](https://prometheus.io/) + [Grafana](https://grafana.com/)

This pipeline is perfect for **data engineers** and **students** interested in learning how to design batch data systems with data quality, observability, and lineage tracking.

---

## **ðŸ—ï¸ Architecture**

![Architecture Diagram](img/architecture.png)

### **Data Flow:**

1. **Data Generator** simulates realistic sales transactions with intentional data quality issues (~20% dirty data)
2. **Bronze Layer** ingests raw JSON data to MinIO without validation
3. **Silver Layer** cleans, validates, and deduplicates data into Delta Lake tables
4. **Quality Checks** validates Silver data using Soda Core with 15+ checks
5. **Gold Layer** creates business aggregations (daily sales, product performance, customer segments)
6. **Trino** provides SQL interface for querying Delta Lake tables
7. **Metabase** visualizes business metrics through interactive dashboards
8. **Marquez** tracks data lineage across the entire pipeline
9. **Grafana** monitors pipeline health and performance metrics

---

## **ðŸ› ï¸ Tech Stack**

| **Component**         | **Technology**                                                              | **Purpose**                                         |
|-----------------------|-----------------------------------------------------------------------------|-----------------------------------------------------|
| **Orchestration**     | [Apache Airflow](https://airflow.apache.org/)                       | DAG scheduling and task management                  |
| **Data Processing**   | [DuckDB](https://duckdb.org/)                                       | Fast analytical processing in-memory                |
| **Data Lake Format**  | [Delta Lake](https://delta.io/)                                            | ACID transactions, time travel, schema evolution    |
| **Object Storage**    | [MinIO](https://min.io/)                                                   | S3-compatible storage for Bronze/Silver/Gold layers |
| **Query Engine**      | [Trino](https://trino.io/)                                                 | Distributed SQL querying on Delta Lake             |
| **Visualization**     | [Metabase](https://www.metabase.com/)                                      | Interactive dashboards and BI                       |
| **Data Quality**      | [Soda Core](https://www.soda.io/)                                          | Data validation and quality checks                  |
| **Data Lineage**      | [Marquez](https://marquezproject.ai/) + [OpenLineage](https://openlineage.io/) | End-to-end data lineage tracking            |
| **Observability**     | [Prometheus](https://prometheus.io/) + [Grafana](https://grafana.com/)    | Metrics collection and visualization                |
| **Data Generation**   | [Faker](https://faker.readthedocs.io/) + [Faker Commerce](https://pypi.org/project/faker-commerce/) | Realistic sales data simulation |

---

## **ðŸ“¦ Project Structure**

```bash
newlinex-sales/
â”œâ”€â”€ airflow/
â”‚   â””â”€â”€ dags/
â”‚       â””â”€â”€ sales_pipeline.py          # Main Airflow DAG
â”œâ”€â”€ config/
â”‚   â””â”€â”€ pipeline_config.yaml           # Pipeline configuration
â”œâ”€â”€ docker/
â”‚   â”œâ”€â”€ airflow/                       # Airflow Docker setup
â”‚   â”œâ”€â”€ grafana/                       # Grafana dashboards & datasources
â”‚   â”œâ”€â”€ marquez/                       # Marquez lineage configuration
â”‚   â”œâ”€â”€ metabase/                      # Metabase setup scripts
â”‚   â”œâ”€â”€ prometheus/                    # Prometheus configuration
â”‚   â”œâ”€â”€ statsd/                        # StatsD metrics mapping
â”‚   â””â”€â”€ trino/                         # Trino catalog configuration
â”œâ”€â”€ docker-compose.yml                 # Docker services orchestration
â”œâ”€â”€ soda/
â”‚   â””â”€â”€ checks.yml                     # Soda Core quality checks
â””â”€â”€ src/
    â”œâ”€â”€ config.py                      # Configuration management
    â”œâ”€â”€ generators/
    â”‚   â””â”€â”€ sales_generator.py         # Synthetic data generator
    â”œâ”€â”€ models/
    â”‚   â””â”€â”€ schemas.py                 # Pydantic validation schemas
    â”œâ”€â”€ processors/
    â”‚   â”œâ”€â”€ base_processor.py          # Abstract base class
    â”‚   â”œâ”€â”€ bronze_processor.py        # Raw data ingestion
    â”‚   â”œâ”€â”€ silver_processor.py        # Data cleaning & deduplication
    â”‚   â”œâ”€â”€ gold_processor.py          # Business aggregations
    â”‚   â””â”€â”€ quality_checker.py         # Data quality validation
    â””â”€â”€ utils/
        â”œâ”€â”€ database.py                # DuckDB connection manager
        â”œâ”€â”€ logger.py                  # Logging configuration
        â”œâ”€â”€ metrics.py                 # Custom Prometheus metrics
        â””â”€â”€ storage.py                 # MinIO/S3 client
```

---

## **ðŸ”§ Setup Instructions**

### **1. Prerequisites**

- **Docker** and **Docker Compose** installed
- Minimum **8GB RAM** recommended
- **Git** for cloning the repository

### **2. Clone the Repository**

```bash
git clone https://github.com/seme555/newlinex.git
cd newlinex
```

### **3. Start All Services**

```bash
docker-compose up -d
```

âš ï¸ **Note:** First startup takes 3-5 minutes to initialize all services. All components are containerized using Docker for easy deployment.

### **4. Access the Services**

| **Service**               | **URL**                          | **Credentials**          |
|---------------------------|----------------------------------|--------------------------|
| **Airflow UI**            | `http://localhost:8080`          | `admin` / `admin`        |
| **Metabase**              | `http://localhost:3000`          | `admin@newlinex.dev` / `NewlineX2024!` |
| **Grafana**               | `http://localhost:3001`          | `admin` / `admin`        |
| **MinIO Console**         | `http://localhost:9001`          | `minioadmin` / `minioadmin` |
| **Trino UI**              | `http://localhost:8081/ui`       | *No Auth*                |
| **Marquez (Lineage)**     | `http://localhost:3002`          | *No Auth*                |
| **Prometheus**            | `http://localhost:9090`          | *No Auth*                |

---

## **ðŸ“¥ Data Generation & Ingestion**

### **1. Sales Data Simulation**

The pipeline generates realistic sales transactions using **Faker** library with the following schema:

```python
{
  "transaction_id": "uuid",
  "customer_id": int,
  "product_id": int,
  "quantity": int,
  "unit_price": float,
  "total_amount": float,
  "transaction_timestamp": "ISO 8601",
  "payment_method": "credit_card | debit_card | cash | digital_wallet",
  "store_id": int,
  "status": "completed | pending | cancelled"
}
```

**Data Quality Issues Injected:**
- ~20% of records contain intentional issues (null values, future dates, negative amounts, mismatched totals, etc.)
- Realistic simulation of real-world data quality problems

### **2. Dimension Tables**

- **Products** (50 items): Generated with faker-commerce
- **Customers** (1,000 users): Includes demographics and segments

### **3. Pipeline Execution**

The Airflow DAG runs **hourly** by default and processes:
- 100 sales transactions per run
- Incremental loading to Bronze layer
- Automatic dimension loading (idempotent)

![Airflow DAG](img/airflow-dag.png)

---

## **ðŸ”„ Data Processing Pipeline**

### **Bronze Layer: Raw Data Ingestion**

- **Purpose:** Store raw data as-is without validation
- **Format:** JSON files in MinIO (s3://bronze/)
- **Strategy:** Accept dirty data for downstream cleaning
- **Idempotency:** Timestamped files prevent overwrites

```python
# Bronze processor accepts all data
processor = BronzeProcessor()
result = processor.process()
# Output: {"key": "sales/sales_20250101_120000.json", "count": 100}
```

### **Silver Layer: Data Cleaning & Deduplication**

- **Purpose:** Clean and validate data with business rules
- **Format:** Delta Lake tables with partitioning
- **Processing:** DuckDB for fast transformations
- **Quality Rules:**
  - Remove null required fields
  - Filter future timestamps
  - Validate payment methods & statuses
  - Check amount calculations
  - Deduplicate by transaction_id

```python
# Silver processor cleans and deduplicates
processor = SilverProcessor()
result = processor.process(bronze_key="sales/sales_20250101_120000.json")
# Output: {
#   "records_read": 100,
#   "records_cleaned": 80,
#   "records_written": 75,
#   "duplicates_removed": 5
# }
```

### **Gold Layer: Business Aggregations**

Gold layer creates three business-critical tables using **parallel processing** (ThreadPoolExecutor):

#### **1. Daily Sales Summary**
```sql
SELECT
    partition_date,
    COUNT(DISTINCT transaction_id) as total_transactions,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_transaction_value,
    SUM(quantity) as total_items_sold,
    completion_rate
FROM silver.sales
GROUP BY partition_date
```

#### **2. Product Performance**
```sql
SELECT
    product_id,
    product_name,
    category,
    SUM(quantity) as units_sold,
    SUM(total_amount) as revenue,
    AVG(unit_price) as avg_selling_price
FROM silver.sales
JOIN bronze.products USING (product_id)
WHERE status = 'completed'
GROUP BY product_id, product_name, category
```

#### **3. Customer Segments**
```sql
SELECT
    customer_id,
    customer_segment,
    COUNT(transaction_id) as purchase_count,
    SUM(total_amount) as total_spend,
    CASE
        WHEN SUM(total_amount) > 1000 THEN 'High Value'
        WHEN SUM(total_amount) > 500 THEN 'Medium Value'
        ELSE 'Low Value'
    END as value_tier
FROM silver.sales
JOIN bronze.customers USING (customer_id)
GROUP BY customer_id, customer_segment
```

**Parallel Processing:**
- All three aggregations run concurrently
- ThreadPoolExecutor with 3 workers

---

## **âœ… Data Quality Validation**

### **Soda Core Checks (15+ Rules)**

The pipeline validates Silver data with comprehensive checks:

```yaml
checks for sales_silver:
  # Volume checks
  - row_count > 0
  - row_count < 10000
  
  # Completeness
  - missing_count(transaction_id) = 0
  - missing_count(customer_id) = 0
  
  # Business rules
  - failed rows: quantity <= 0
  - failed rows: total_amount <= 0
  - failed rows: total != quantity * unit_price
  
  # Validity
  - duplicate_count(transaction_id) = 0
  - valid payment_method values
  - valid status values
  
  # Freshness
  - freshness(transaction_timestamp) < 2h
  
  # Statistical
  - avg(total_amount) between 50 and 2000

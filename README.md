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

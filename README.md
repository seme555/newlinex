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

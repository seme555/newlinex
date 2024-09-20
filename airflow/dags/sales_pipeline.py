"""
Sales Delta Pipeline DAG - Interface Inheritance Pattern

Design Principles:
- All processors inherit from BaseProcessor
- Consistent error handling and metrics
- Idempotent operations (safe to re-run)
- Parallel Gold aggregations using ThreadPoolExecutor
- Proper task dependencies and branching
"""
import sys
from datetime import datetime, timedelta
from typing import Dict, Any

from airflow.decorators import dag, task
from airflow.operators.python import BranchPythonOperator
from airflow.exceptions import AirflowSkipException
from airflow.lineage.entities import File

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
from airflow.models import DagRun

# Add src to path
sys.path.insert(0, '/opt/airflow')

from src.config import get_config
from src.processors.bronze_processor import BronzeProcessor
from src.processors.silver_processor import SilverProcessor
from src.processors.gold_processor import GoldProcessor
from src.processors.quality_checker import QualityChecker
from src.utils.logger import get_logger

logger = get_logger(__name__)

# DAG configuration
default_args = {
    'owner': get_config('pipeline', 'name', default='airflow'),
    'retries': get_config('pipeline', 'retries', default=1),

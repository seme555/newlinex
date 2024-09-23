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
    'retry_delay': timedelta(
        minutes=get_config('pipeline', 'retry_delay_minutes', default=1)
    ),
    'execution_timeout': timedelta(minutes=30),
    'email_on_failure': False,
    'email_on_retry': False,
}


@dag(
    dag_id=get_config('pipeline', 'name', default='sales_delta_pipeline'),
    schedule_interval=get_config('pipeline', 'schedule', default='@hourly'),
    start_date=datetime.strptime(
        get_config('pipeline', 'start_date', default='2024-01-01'),
        '%Y-%m-%d'
    ),
    catchup=get_config('pipeline', 'catchup', default=False),
    default_args=default_args,
    tags=["sales", "delta", "incremental", "interface-inheritance"],
    description="Incremental sales data pipeline",
    max_active_runs=1,  # Prevent concurrent runs
    doc_md="""
    # Sales Delta Pipeline
    
    **Architecture**: Bronze â†’ Silver â†’ Gold (Medallion)
    
    **Design Pattern**: Interface Inheritance
    - All processors inherit from `BaseProcessor`
    - Shared authentication, error handling, and metrics
    - Consistent interface across all layers
    
    **Flow**:
    1. **Bronze**: Ingest raw sales data (with dirty data)
    2. **Bronze**: Load dimension tables (idempotent)
    3. **Silver**: Clean, validate, and deduplicate to Delta Lake
    4. **Quality**: Run Soda Core data quality checks
    5. **Gold**: Aggregate business metrics (parallel processing)
    
    **Idempotency**: Safe to re-run at any step
    """
)
def sales_delta_pipeline():
    """
    Sales data pipeline with Bronze-Silver-Gold architecture.
    Uses Interface Inheritance pattern for clean, maintainable code.
    """
    
    @task(
        task_id='ingest_to_bronze',
        inlets=[],
        outlets=[File(url="s3://bronze/sales_raw/")]
    )
    def ingest_sales_data() -> Dict[str, Any]:
        """
        Ingest incremental sales to Bronze layer.
        
        Returns:
            {"key": s3_key, "count": record_count, "status": "success"}
        """
        try:
            processor = BronzeProcessor()
            result = processor.process()
            
            # Skip downstream if no data
            if result.get('count', 0) == 0:
                logger.warning("No sales data generated, skipping pipeline")
                raise AirflowSkipException("No data to process")
            
            logger.info(
                f"âœ“ Bronze ingestion complete: {result['count']} records â†’ {result['key']}"
            )
            
            return result
            
        except AirflowSkipException:
            raise
        except Exception as e:
            logger.error(f"Bronze ingestion failed: {e}")
            raise
    
    @task
    def load_dimension_tables() -> Dict[str, Any]:
        """
        Load product and customer dimensions (idempotent).
        
        Returns:
            {"status": "loaded" | "skipped", "products": int, "customers": int}
        """
        try:
            processor = BronzeProcessor()
            result = processor.load_dimensions()
            
            if result['status'] == 'skipped':
                logger.info("âœ“ Dimensions already loaded")
            else:
                logger.info(
                    f"âœ“ Loaded {result['products']} products and "
                    f"{result['customers']} customers"
                )
            
            return result
            
        except Exception as e:
            logger.error(f"Dimension loading failed: {e}")
            raise
    
    @task(
        task_id='transform_to_silver',
        inlets=[File(url="s3://bronze/sales_raw/")],
        outlets=[File(url="s3://silver/sales_cleaned/")]
    )
    def process_to_silver(bronze_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process Bronze â†’ Silver with cleaning and deduplication.
        
        Args:
            bronze_result: Output from ingest_sales_data task
        
        Returns:
            {
                "records_read": int,
                "records_cleaned": int,
                "records_written": int,
                "duplicates_removed": int,
                "status": "success"
            }

"""Gold layer: Business aggregations as Delta tables with parallel processing."""
from datetime import datetime
from typing import Dict, Any, List, Callable, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import pyarrow as pa
import pyarrow.compute as pc
from deltalake import DeltaTable, write_deltalake
from deltalake.exceptions import TableNotFoundError

from src.processors.base_processor import BaseProcessor
from src.utils.database import DuckDBClient
from src.utils.metrics import track_table_size


class GoldProcessor(BaseProcessor):
    """
    Gold layer processor - creates business aggregations.
    Uses ThreadPoolExecutor for parallel table processing.
    """
    
    def _validate_config(self) -> None:
        """Validate Gold-specific configuration."""
        self.bronze_bucket = self._get_bucket('bronze')
        self.silver_bucket = self._get_bucket('silver')
        self.gold_bucket = self._get_bucket('gold')
        self.storage_options = self.storage.get_storage_options()
        
        self.logger.info(
            f"Gold config: bronze={self.bronze_bucket}, "
            f"silver={self.silver_bucket}, gold={self.gold_bucket}"
        )
    
    def process(self, **kwargs) -> Dict[str, Any]:
        """
        Create daily business metrics as Delta tables.
        Processes all aggregations in parallel using ThreadPoolExecutor.
        
        Returns:
            {
                "daily_sales_summary": {"status": "success", "rows": 1},
                "product_performance": {"status": "success", "rows": 50},
                "customer_segments": {"status": "success", "rows": 150},
                "overall_status": "success"
            }
        """
        try:
            date = datetime.utcnow().strftime("%Y-%m-%d")
            
            # Load Silver data once (shared across all aggregations)
            sales_df = self._load_silver_data()
            
            if sales_df is None or len(sales_df) == 0:
                self.logger.warning("No Silver data available, skipping aggregation")
                return {
                    "status": "skipped",
                    "reason": "no_silver_data"
                }
            
            # Define aggregations to run in parallel
            aggregations: List[tuple[str, Callable]] = [
                ('daily_sales_summary', lambda: self._aggregate_daily_sales(sales_df, date)),
                ('product_performance', lambda: self._aggregate_product_performance(sales_df, date)),
                ('customer_segments', lambda: self._aggregate_customer_segments(sales_df, date)),
            ]
            
            # Execute aggregations in parallel
            results = self._execute_parallel_aggregations(aggregations)
            
            # Determine overall status
            overall_status = "success" if all(
                r.get("status") == "success" for r in results.values()
            ) else "partial_failure"
            
            results["overall_status"] = overall_status
            
            success_count = len([
                r for k, r in results.items()
                if k != "overall_status" and isinstance(r, dict) and r.get("status") == "success"
            ])
            self.logger.info(
                f"âœ“ Gold aggregation complete: {overall_status} "
                f"({success_count} of {len(aggregations)} succeeded)"
            )
        
            return results
            
        except Exception as e:
            self._handle_error(e, "gold_aggregation")
    
    def _load_silver_data(self, date: str = None) -> Optional[pa.Table]:
        """Load only today's partition for incremental aggregation."""
        silver_path = f"s3://{self.silver_bucket}/sales"
        
        if date is None:
            date = datetime.utcnow().strftime("%Y-%m-%d")
        
        try:
            dt = DeltaTable(silver_path, storage_options=self.storage_options)
            
            sales_arrow = dt.to_pyarrow_table(
                filters=[("partition_date", "=", date)]
            )
            
            self.logger.info(
                f"Loaded {sales_arrow.num_rows} records for partition_date={date}"
            )
            return sales_arrow
            
        except TableNotFoundError:
            self.logger.warning("Silver table does not exist yet")
            return None
            
        except Exception as e:
            self.logger.error(
                f"Failed to load Silver table: {type(e).__name__}: {e}"
            )
            raise
    
    def _execute_parallel_aggregations(
        self, 
        aggregations: List[tuple[str, Callable]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Execute multiple aggregations in parallel using ThreadPoolExecutor.
        
        Args:
            aggregations: List of (name, function) tuples
        
        Returns:
            Dict mapping aggregation name to result
        """
        results = {}
        
        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=3) as executor:
            # Submit all aggregations
            future_to_agg = {
                executor.submit(agg_func): name 
                for name, agg_func in aggregations
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_agg):
                agg_name = future_to_agg[future]
                
                try:
                    result = future.result()
                    results[agg_name] = result
                    self.logger.info(f"âœ“ Completed {agg_name}")
                    
                except Exception as e:
                    self.logger.error(
                        f"Failed {agg_name}: {type(e).__name__}: {e}",
                        exc_info=True
                    )
                    results[agg_name] = {
                        "status": "failed",
                        "error": str(e)
                    }
        
        return results
    
    def _aggregate_daily_sales(
        self, 
        sales_arrow: pa.Table,
        date: str
    ) -> Dict[str, Any]:
        try:
            with DuckDBClient() as conn:
                conn.register('sales', sales_arrow)
                
                result_arrow = conn.execute(f"""
                    SELECT 
                        partition_date,
                        COUNT(DISTINCT transaction_id) as total_transactions,
                        COUNT(DISTINCT customer_id) as unique_customers,
                        SUM(total_amount) as total_revenue,
                        AVG(total_amount) as avg_transaction_value,
                        SUM(quantity) as total_items_sold,
                        COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_transactions,
                        COUNT(CASE WHEN status = 'cancelled' THEN 1 END) as cancelled_transactions,
                        ROUND(100.0 * COUNT(CASE WHEN status = 'completed' THEN 1 END) /
                            NULLIF(COUNT(*), 0), 2) as completion_rate,
                        CURRENT_TIMESTAMP as created_at,
                        '{date}' as data_date
                    FROM sales
                    WHERE partition_date = '{date}'
                    GROUP BY partition_date
                """).arrow()
            
            if result_arrow.num_rows == 0:
                self.logger.warning("No data for daily_sales_summary")
                return {"status": "skipped", "rows": 0}
            
            self._upsert_to_delta(
                table_name='daily_sales_summary',
                arrow_table=result_arrow,
                merge_keys=['data_date'],

"""Custom metrics for pipeline observability."""
import time
import os
from functools import wraps
from typing import Callable, Optional
from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry, push_to_gateway
from src.utils.logger import get_logger
from src.config import get_config

logger = get_logger(__name__)

# Pushgateway configuration
PUSHGATEWAY_URL = get_config('observability', 'prometheus_pushgateway', default='prometheus-pushgateway:9091')
JOB_NAME = get_config('observability', 'job_name', default='sales_pipeline')

# Metrics registry
registry = CollectorRegistry()


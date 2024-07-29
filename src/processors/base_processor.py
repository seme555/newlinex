"""Base processor implementing shared logic for all data layers."""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from src.utils.storage import StorageClient
from src.utils.logger import get_logger
from src.utils.metrics import track_records, push_metrics
from src.config import get_config


class BaseProcessor(ABC):
    """
    Abstract base class for all processors.
    Enforces interface contract and handles common operations.
    
    Design Pattern: Interface Inheritance
    - Shared authentication/storage logic
    - Consistent error handling
    - Standardized metric tracking

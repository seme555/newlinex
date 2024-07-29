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
    """
    
    def __init__(self):
        self.storage = StorageClient()
        self.logger = get_logger(self.__class__.__name__)
        self._validate_config()
        self.logger.info(f"âœ“ Initialized {self.__class__.__name__}")
    
    @abstractmethod
    def _validate_config(self) -> None:
        """
        Validate processor-specific configuration.
        Must be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def process(self, **kwargs) -> Dict[str, Any]:

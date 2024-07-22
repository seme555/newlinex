"""Configuration management for the pipeline."""
import os
import yaml
from typing import Dict, Any
from pathlib import Path


class Config:
    """Pipeline configuration singleton."""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._load_config()
        return cls._instance
    
    @classmethod
    def _load_config(cls):
        """Load and validate configuration."""
        config_path = Path("/opt/airflow/config/pipeline_config.yaml")
        
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            cls._config = yaml.safe_load(f)
        
        cls._config = cls._replace_env_vars(cls._config)
        
        # Validate required keys
        required_keys = [
            ('s3', 'endpoint'),
            ('s3', 'access_key'),

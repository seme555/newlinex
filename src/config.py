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

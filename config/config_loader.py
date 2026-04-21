"""
Configuration Loader
"""
import yaml
import os
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class Config:
    """Singleton configuration loader"""
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._config is None:
            self._load_config()

    def _load_config(self):
        """Load configuration from YAML file"""
        config_path = Path(__file__).parent / "analysis_config.yaml"
        try:
            with open(config_path, 'r') as f:
                self._config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {config_path}")
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            # Provide default configuration
            self._config = self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration if file loading fails"""
        return {
            "agents": {
                "analyst": {"temperature": 0.2, "max_iterations": 15, "allow_delegation": False},
                "fundamental": {"temperature": 0.2, "max_iterations": 20, "allow_delegation": True},
                "trader": {"temperature": 0.4, "max_iterations": 15, "allow_delegation": True},
                "planner": {"temperature": 0.3, "max_iterations": 10, "allow_delegation": False},
                "manager": {"temperature": 0.5, "max_iterations": 25}
            },
            "markets": {
                "us": {"cache_duration_seconds": 300, "rate_limit_calls": 10, "rate_limit_period_seconds": 60},
                "india": {"cache_duration_seconds": 600, "rate_limit_calls": 5, "rate_limit_period_seconds": 60}
            },
            "analysis": {
                "parallel_execution": True,
                "enable_memory": True,
                "enable_planning": True,
                "verbose": True
            },
            "retry": {
                "max_attempts": 3,
                "min_wait_seconds": 1,
                "max_wait_seconds": 10
            },
            "cache": {
                "enabled": True,
                "max_size": 100,
                "ttl_minutes": 5
            }
        }

    def get(self, key_path: str, default=None):
        """
        Get configuration value by dot-notation path

        Example: config.get('agents.analyst.temperature')
        """
        keys = key_path.split('.')
        value = self._config
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default
            if value is None:
                return default
        return value

    @property
    def all(self) -> Dict[str, Any]:
        """Get all configuration"""
        return self._config


# Global configuration instance
config = Config()

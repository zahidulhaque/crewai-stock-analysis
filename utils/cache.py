"""
Caching utilities for API calls
"""
from functools import wraps
from datetime import datetime, timedelta
from typing import Any, Callable, Dict
import hashlib
import json
import logging

logger = logging.getLogger(__name__)


class SimpleCache:
    """Simple time-based cache implementation"""

    def __init__(self, ttl_seconds: int = 300, max_size: int = 100):
        """
        Initialize cache

        Args:
            ttl_seconds: Time-to-live in seconds
            max_size: Maximum number of cached items
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.ttl_seconds = ttl_seconds
        self.max_size = max_size

    def _make_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Create cache key from function name and arguments"""
        # Create a deterministic string from args and kwargs
        key_data = {
            'func': func_name,
            'args': args,
            'kwargs': sorted(kwargs.items())
        }
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_str.encode()).hexdigest()

    def get(self, key: str) -> Any:
        """Get value from cache if not expired"""
        if key in self._cache:
            entry = self._cache[key]
            if datetime.now() < entry['expires_at']:
                logger.debug(f"Cache hit for key: {key[:16]}...")
                return entry['value']
            else:
                # Expired, remove it
                logger.debug(f"Cache expired for key: {key[:16]}...")
                del self._cache[key]
        return None

    def set(self, key: str, value: Any):
        """Set value in cache with TTL"""
        # Implement simple LRU by removing oldest if at max size
        if len(self._cache) >= self.max_size:
            # Remove oldest entry
            oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k]['created_at'])
            del self._cache[oldest_key]
            logger.debug(f"Cache full, removed oldest entry")

        self._cache[key] = {
            'value': value,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(seconds=self.ttl_seconds)
        }
        logger.debug(f"Cached value for key: {key[:16]}... (TTL: {self.ttl_seconds}s)")

    def clear(self):
        """Clear all cache entries"""
        self._cache.clear()
        logger.info("Cache cleared")

    def stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        valid_entries = sum(1 for entry in self._cache.values()
                          if datetime.now() < entry['expires_at'])
        return {
            'total_entries': len(self._cache),
            'valid_entries': valid_entries,
            'expired_entries': len(self._cache) - valid_entries,
            'max_size': self.max_size,
            'ttl_seconds': self.ttl_seconds
        }


# Global cache instances
_stock_price_cache = SimpleCache(ttl_seconds=300, max_size=100)  # 5 minutes
_financial_data_cache = SimpleCache(ttl_seconds=600, max_size=50)  # 10 minutes


def cached(cache: SimpleCache = None, ttl_seconds: int = None):
    """
    Decorator to cache function results

    Args:
        cache: Cache instance to use (creates new one if None)
        ttl_seconds: Override TTL for this specific function
    """
    if cache is None:
        cache = SimpleCache(ttl_seconds=ttl_seconds or 300)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            cache_key = cache._make_key(func.__name__, args, kwargs)

            # Try to get from cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                logger.info(f"Using cached result for {func.__name__}")
                return cached_value

            # Call function and cache result
            logger.info(f"Cache miss for {func.__name__}, executing function")
            result = func(*args, **kwargs)
            cache.set(cache_key, result)
            return result

        return wrapper
    return decorator


def get_stock_price_cache() -> SimpleCache:
    """Get stock price cache instance"""
    return _stock_price_cache


def get_financial_data_cache() -> SimpleCache:
    """Get financial data cache instance"""
    return _financial_data_cache


def clear_all_caches():
    """Clear all cache instances"""
    _stock_price_cache.clear()
    _financial_data_cache.clear()
    logger.info("All caches cleared")

import time
from typing import List, Any, Callable, TypeVar
from loguru import logger
from functools import wraps

T = TypeVar('T')

def rate_limit(calls: int, period: float):
    """Rate limiting decorator that allows 'calls' number of calls per 'period' seconds."""
    min_interval = period / calls
    last_called = [0.0]  # Using list to allow modification in closure

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

def batch_process(items: List[Any], batch_size: int, process_func: Callable[[List[Any]], List[T]]) -> List[T]:
    """Process items in batches to avoid overwhelming the API."""
    results = []
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        try:
            batch_results = process_func(batch)
            results.extend(batch_results)
            logger.debug(f"Processed batch {i//batch_size + 1} successfully")
        except Exception as e:
            logger.error(f"Error processing batch {i//batch_size + 1}: {str(e)}")
            raise
    return results

def retry_with_exponential_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0
):
    """Retry decorator with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for retry in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if retry == max_retries - 1:
                        logger.error(f"Max retries ({max_retries}) reached. Last error: {str(e)}")
                        raise
                    logger.warning(f"Attempt {retry + 1} failed: {str(e)}. Retrying...")
                    time.sleep(delay)
                    delay = min(delay * exponential_base, max_delay)
        return wrapper
    return decorator
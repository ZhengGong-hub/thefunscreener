import json
import logging
import os
import sys
import time
from collections.abc import Callable
from datetime import datetime
from functools import wraps
import asyncio

# Configure logging levels based on environment
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = os.getenv("LOG_FORMAT", "json")  # Options: json, text

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure root logger
root_logger = logging.getLogger()
root_logger.setLevel(LOG_LEVEL)

# Clear existing handlers to avoid duplication
if root_logger.handlers:
    root_logger.handlers.clear()

# Custom JSON formatter
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if available
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        # Add extra fields from record
        if hasattr(record, "extra"):
            log_record.update(record.extra)

        return json.dumps(log_record)

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
if LOG_FORMAT.lower() == "json":
    console_handler.setFormatter(JsonFormatter())
else:
    console_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
root_logger.addHandler(console_handler)

# Create file handler for all logs
file_handler = logging.FileHandler(f"logs/thefunscreener_{datetime.now().strftime('%Y%m%d')}.log")
if LOG_FORMAT.lower() == "json":
    file_handler.setFormatter(JsonFormatter())
else:
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
root_logger.addHandler(file_handler)

# Create separate file handler for errors
error_handler = logging.FileHandler(f"logs/thefunscreener_errors_{datetime.now().strftime('%Y%m%d')}.log")
error_handler.setLevel(logging.ERROR)
if LOG_FORMAT.lower() == "json":
    error_handler.setFormatter(JsonFormatter())
else:
    error_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
root_logger.addHandler(error_handler)

def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name."""
    return logging.getLogger(name)

def log_execution_time(func: Callable) -> Callable:
    """Decorator to log function execution time."""
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        start_time = time.time()
        logger.info(f"Starting {func.__name__}")
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"Completed {func.__name__} in {execution_time:.2f}s")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(
                f"Failed {func.__name__} after {execution_time:.2f}s",
                exc_info=True,
                extra={"error_type": type(e).__name__}
            )
            raise

    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        start_time = time.time()
        logger.info(f"Starting {func.__name__}")
        try:
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"Completed {func.__name__} in {execution_time:.2f}s")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(
                f"Failed {func.__name__} after {execution_time:.2f}s",
                exc_info=True,
                extra={"error_type": type(e).__name__}
            )
            raise

    # Return the appropriate wrapper based on whether the function is async or not
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper

def log_api_call(func: Callable) -> Callable:
    """Decorator to log API calls with request and response details."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        start_time = time.time()

        # Log request
        logger.info(
            f"API call to {func.__name__}",
            extra={"request_params": str(kwargs)}
        )

        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time

            # Log response (truncated if too large)
            response_str = str(result)
            if len(response_str) > 1000:
                response_str = response_str[:1000] + "... [truncated]"

            logger.info(
                f"API response from {func.__name__}",
                extra={
                    "execution_time": f"{execution_time:.2f}s",
                    "response": response_str
                }
            )
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(
                f"API call to {func.__name__} failed",
                exc_info=True,
                extra={
                    "execution_time": f"{execution_time:.2f}s",
                    "error_type": type(e).__name__
                }
            )
            raise
    return wrapper

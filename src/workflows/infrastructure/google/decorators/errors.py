from functools import wraps
import logging
from typing import Callable, Any
from src.shared.utils.logs.logger import Logger
from src.shared.dependencies.container import Container
from googleapiclient.errors import HttpError

def google_api_error_handler(module: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except HttpError as e:
                error = e.error_details[0]["message"]
                logger: Logger = Container.resolve("logger")
                logger.log(
                    message=f"Error in {func.__name__}::::: {error} :::::",
                    level=logging.WARN,
                    name=f"{module}.{func.__name__}",
                    exc_info=False
                )
                return 
            except Exception as e:
                logger: Logger = Container.resolve("logger")
                logger.log(
                    message=f"Error in {func.__name__}::::: {e} :::::",
                    level=logging.ERROR,
                    name=f"{module}.{func.__name__}",
                    exc_info=True
                )
                raise  
        return wrapper
    
    return decorator
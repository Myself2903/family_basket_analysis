import logging
import pandas as pd
from pathlib import Path
from functools import wraps
from time import perf_counter
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec('P')
R = TypeVar('R')

def timer(fn: Callable[P, R]) -> Callable[P, R]:
    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start_time = perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            end_time = perf_counter()

            logger = logging.getLogger(__name__)
            logger.info(f'Execution time: {end_time-start_time:.2f}')

    return wrapper

def load_csv(file_path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found")



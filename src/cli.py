from src.config import CATEGORICAL_COLUMNS, NUMERIC_COLUMNS
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def setup_logger(verbose: bool = False) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    log_level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(log_level)

def print_separator() -> None:
    logger.debug("-" * 100)

def print_title(title: str) -> None:
    logger.debug(f'\033[1m {title:=^50} \033[0m')

def show_data_structure(data: pd.DataFrame | pd.Series, n_rows:int = 5) -> None:
    print_separator()
    logger.debug(f'data shape: {data.shape}')
    data.info()
    print_separator()
    print(data.sample(min(n_rows, len(data))))
    print_separator()

def show_unique_values(data: pd.DataFrame, columns: list[str] | None = None) -> None:
    columns = data.columns.to_list() if columns is None else columns
   
    for column in columns:
        print_separator()
        logger.debug(f'======== Describing {column} ========')
        print(data[column].value_counts())

def describe_numerical_columns(data: pd.DataFrame) -> None:
    logger.debug('======== Numeric columns resume ========')
    print(data[NUMERIC_COLUMNS].describe().round(2))
    print_separator()

def describe_categorical_columns(data: pd.DataFrame) -> None:
    print_title(' DESCRIBING CATEGORICAL COLUMNS ')
    show_unique_values(data, CATEGORICAL_COLUMNS)
    print_separator()
    logger.debug('======== Categorical columns resume ========')
    print(data[CATEGORICAL_COLUMNS].describe())
    print_separator()

def describe_added_columns(data: pd.DataFrame) -> None:
    print_title(' ADDED COLUMNS ')
    show_data_structure(data[[
        'price_variation_range',
        'price_variation_percentage',
        'anio',
        'mes',
        'anio_mes'
    ]])
    

from src.config import NUMERIC_COLUMNS, DATE_COLUMNS
import dateparser
import pandas as pd

def transform_price_to_float(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column].str.replace(',', ''))

    return df

def transform_str_date_to_date(data:pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    for column in DATE_COLUMNS:
        df[column] = df[column].apply(
            lambda x: dateparser.parse(x, languages=['es'])
        )
   
    return df

def run_pipeline(data: pd.DataFrame) -> pd.DataFrame:
    """Aplica todas las transformaciones en cadena."""
    return (
        data
        .pipe(transform_price_to_float)
        .pipe(transform_str_date_to_date)
    )

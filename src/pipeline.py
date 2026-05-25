from src.config import MONTHS_MAPPING, NUMERIC_COLUMNS, DATE_COLUMNS
import pandas as pd

def transform_price_to_float(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column].str.replace(',', ''))

    return df

def transform_str_date_to_date(data:pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    for column in DATE_COLUMNS:
        df[column] = (
            df[column]
            .str.split(',').str[1] # deletes week day
            .str.strip()
            .str.lower()
            .str.replace('de', '') # deletes 'de' statements
            .apply( # maps months names to number format
                lambda x: '-'.join([ str(MONTHS_MAPPING.get(date_info, date_info) ) for date_info in x.split('  ') ]) 
            )
        )

        df[column] = pd.to_datetime(df[column], format='%d-%m-%Y')
   
    return df

def run_pipeline(data: pd.DataFrame) -> pd.DataFrame:
    """Aplica todas las transformaciones en cadena."""
    return (
        data
        .pipe(transform_price_to_float)
        .pipe(transform_str_date_to_date)
    )

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

def remove_city_from_market(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    df['Mercados'] = (
        df['Mercados']
        .str.split(',').str[1]
        .str.strip()
    )

    return df

def add_price_variation_columns(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    minimum_price_column, maximum_price_column, average_price_column = NUMERIC_COLUMNS

    df["price_variation_range"] = (
        df[maximum_price_column] - df[minimum_price_column]
    )

    df["price_variation_percentage"] = (
        df["price_variation_range"] / df[average_price_column]
    ) * 100

    return df

def add_date_parts(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    df["anio"] = df["Fecha_inicial"].dt.year
    df["mes"] = df["Fecha_inicial"].dt.month
    df["anio_mes"] = df["Fecha_inicial"].dt.to_period("M")

    return df

def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    return (
        data
        .pipe(transform_price_to_float)
        .pipe(transform_str_date_to_date)
        .pipe(remove_city_from_market)
        .pipe(add_price_variation_columns)
        .pipe(add_date_parts)
    )

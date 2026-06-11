import pandas as pd
from src.config import MONTHS_MAPPING, NUMERIC_COLUMNS, DATE_COLUMNS

###################################
######### Cleaning data ###########
###################################
def transform_price_to_float(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column].str.replace(',', ''))

    return df

def transform_str_date_to_date(data:pd.DataFrame) -> pd.DataFrame:
    df = data.copy()

    # regex expression to delete dayweek
    days_regex = r'(lunes|martes|miércoles|miercoles|jueves|viernes|sábado|sabado|domingo)(,\s*|\s+)'
    for column in DATE_COLUMNS:
        df[column] = (
            df[column]
            .str.strip()
            .str.lower()
            .str.replace(days_regex, '', regex=True)
            .str.replace('de', '') # deletes 'de' statements
            .apply( # maps months names to number format
                lambda x: '-'.join([ str(MONTHS_MAPPING.get(date_info, date_info) ) for date_info in x.split() ]) 
            )
        )

        try:
            df[column] = pd.to_datetime(df[column], format='%d-%m-%Y')
        except ValueError as e:

            for i, value in df[column].items():
                try:
                    pd.to_datetime(value, format='%d-%m-%Y')
                except ValueError:
                    raise ValueError(f"Entry {i} with value '{data[column].iloc[i]}' in column {column} has an unknown format dd-mm-yyyy or day-month-year expected")
   
    return df

def remove_city_from_market(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()

    # if entry does not include ',' it is replaced with NaN so we use an auxiliar variable
    extracted_market = df['Mercados'].str.split(',').str[1]
    df['Mercados'] = extracted_market.fillna(df['Mercados']).str.strip().astype(str)

    return df

def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    return (
        data
        .pipe(transform_price_to_float)
        .pipe(transform_str_date_to_date)
        .pipe(remove_city_from_market)
    )

####################################
######### Extending data ###########
####################################

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


def extend_data(data: pd.DataFrame) -> pd.DataFrame:
    return (
        data
        .pipe(add_price_variation_columns)
        .pipe(add_date_parts)
    ) 

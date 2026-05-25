from pathlib import Path
import pandas as pd

def print_separator():
    print("-"*50)

def load_csv(file_path: Path) -> pd.DataFrame:
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found")
   
def show_data_structure(data: pd.DataFrame, n_rows:int = 5) -> None:
    print_separator()
    print(data.shape)
    print(data.info())
    print_separator()
    print(data.head(n_rows))

def show_unique_values(data: pd.DataFrame, columns: list[str] | None = None) -> None:
    if columns is None:
        columns = data.columns.to_list()
   
    for column in columns:
        print_separator()
        print(data[column].value_counts())

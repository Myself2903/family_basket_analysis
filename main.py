from src.config import FILE_PATH
from src.pipeline import run_pipeline
from src.utils import load_csv, show_data_structure
import time
   
def main() -> None:

    print(f"================= DESCRIBING DATA =================")
    print(f'FILE: {FILE_PATH.name}')

    data = load_csv(FILE_PATH)

    # show_data_structure(data)
    # show_unique_values(data)
   
    start = time.perf_counter()
    data_cleaned = run_pipeline(data)

    # show_data_structure(data)
    show_data_structure(data_cleaned)
    end = time.perf_counter()
    print(f"Execution time: {end - start:.4f} seconds")

if __name__ == '__main__':
    main()


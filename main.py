from src.config import FILE_PATH
from src.pipeline import clean_data
from src.utils import load_csv, show_data_structure
from src.visualizations import build_price_index, plot_price_index

def main() -> None:

    print(f"================= DESCRIBING DATA =================")
    print(f'FILE: {FILE_PATH.name}')

    data = load_csv(FILE_PATH)

    # show_data_structure(data)
    # show_unique_values(data)

    data_cleaned = clean_data(data)

    show_data_structure(data_cleaned)

    print(f"================= VISUALIZATIONS =================")
    index_series, base_period = build_price_index(data_cleaned)
    output_path = plot_price_index(index_series, base_period)
    print(f"Gráfico A (evolución temporal) guardado en: {output_path}")

if __name__ == '__main__':
    main()


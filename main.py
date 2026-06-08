from src.config import FILE_PATH
from src.pipeline import clean_data, extend_data
from src.utils import load_csv, show_data_structure
from src.visualizations import (
    build_price_index,
    plot_price_index,
    build_city_price_index,
    plot_city_price_index,
    build_category_volatility,
    plot_category_volatility,
)

def main() -> None:

    print(f"================= DESCRIBING DATA =================")
    print(f'FILE: {FILE_PATH.name}')

    data = load_csv(FILE_PATH)

    # show_data_structure(data)
    # show_unique_values(data)

    data_cleaned = clean_data(data)

    show_data_structure(data_cleaned)

    data_cleaned = extend_data(data_cleaned)

    print(f"================= VISUALIZATIONS =================")
    index_series, base_period = build_price_index(data_cleaned)
    output_path = plot_price_index(index_series, base_period)
    print(f"Gráfico A (evolución temporal) guardado en: {output_path}")

    city_index, n_common = build_city_price_index(data_cleaned)
    city_output_path = plot_city_price_index(city_index, n_common)
    print(f"Gráfico B (comparación entre ciudades) guardado en: {city_output_path}")

    category_order, _ = build_category_volatility(data_cleaned)
    volatility_output_path = plot_category_volatility(data_cleaned, category_order)
    print(f"Gráfico C (volatilidad por categoría) guardado en: {volatility_output_path}")

if __name__ == '__main__':
    main()


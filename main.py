import argparse
from functools import wraps
from time import perf_counter
from typing import Callable, ParamSpec, TypeVar
from src import (
    FILE_PATH,
    cli,
    pipeline as pipe,
    visualizations as vis
)

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

            cli.logger.info(f'Execution time: {end_time-start_time:.2f}')

    return wrapper

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "-v", "--verbose",
            action="store_true",
            help="Enables description output in CLI"
    )

    return parser.parse_args()

@timer 
def main() -> None:
    args = parse_args()
    cli.setup_logger(args.verbose)

    cli.logger.info(f'Source File: {FILE_PATH.name}')

    data = pipe.load_csv(FILE_PATH)

    if args.verbose:
        cli.print_title(' DATASET RESUME ')
        cli.show_data_structure(data)
  
    data_cleaned = pipe.clean_data(data)

    if args.verbose:
        cli.print_title(' CLEANED DATASET RESUME ')
        cli.show_data_structure(data_cleaned)
        cli.describe_categorical_columns(data_cleaned)
        cli.describe_numerical_columns(data_cleaned)

    data_cleaned = pipe.extend_data(data_cleaned)
    
    if args.verbose:
        cli.describe_added_columns(data_cleaned)

    cli.logger.info('GENERATING DATA PLOTS')

    index_series, base_period = vis.build_price_index(data_cleaned)
    output_path = vis.plot_price_index(index_series, base_period)

    city_index, n_common = vis.build_city_price_index(data_cleaned)
    city_output_path = vis.plot_city_price_index(city_index, n_common)

    category_order, _ = vis.build_category_volatility(data_cleaned)
    volatility_output_path = vis.plot_category_volatility(data_cleaned, category_order)

    print(f"================= VISUALIZATIONS =================")
    print(f"Gráfico A (evolución temporal) guardado en: {output_path}")
    print(f"Gráfico B (comparación entre ciudades) guardado en: {city_output_path}")
    print(f"Gráfico C (volatilidad por categoría) guardado en: {volatility_output_path}")

if __name__ == '__main__':
    main()


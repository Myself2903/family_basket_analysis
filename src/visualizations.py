from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.config import FIGURES_DIR


def build_price_index(
    data: pd.DataFrame,
    period_column: str = "anio_mes",
    price_column: str = "Precio_medio",
    product_column: str = "Productos",
) -> tuple[pd.Series, pd.Period]:
    """Builds a base-100 price index using price relatives (Carli style).

    Each product is normalized against its own price in the base period and
    then the relatives are averaged. This prevents expensive products from
    dominating the index, which a raw average of heterogeneous products would.
    """
    df = data.copy()

    # average price per product per month (smooths weekly noise)
    monthly = (
        df.groupby([product_column, period_column])[price_column]
        .mean()
        .reset_index()
    )

    base_period = monthly[period_column].min()
    base_prices = (
        monthly.loc[monthly[period_column] == base_period]
        .set_index(product_column)[price_column]
    )

    # keep only products present in the base period so the base is comparable
    monthly = monthly[monthly[product_column].isin(base_prices.index)].copy()
    monthly["price_relative"] = (
        monthly[price_column] / monthly[product_column].map(base_prices) * 100
    )

    index_series = (
        monthly.groupby(period_column)["price_relative"].mean().rename("indice")
    )

    return index_series, base_period


def plot_price_index(
    index_series: pd.Series,
    base_period: pd.Period,
    output_dir: Path = FIGURES_DIR,
) -> Path:
    """Plots the base-100 price index as a time series and saves it as PNG."""
    output_dir.mkdir(parents=True, exist_ok=True)

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(11, 6))

    x = index_series.index.to_timestamp()
    final_value = index_series.iloc[-1]
    variation = final_value - 100

    ax.plot(x, index_series.values, color="#1f4e79", linewidth=2.4)
    ax.axhline(100, color="grey", linestyle="--", linewidth=1)

    # highlight the final value, which is the headline of the chart
    ax.scatter(x[-1], final_value, color="#c0392b", zorder=5)
    ax.annotate(
        f"{final_value:.1f}\n(+{variation:.1f}% vs base)",
        xy=(x[-1], final_value),
        xytext=(-10, 18),
        textcoords="offset points",
        ha="right",
        fontsize=10,
        fontweight="bold",
        color="#c0392b",
    )

    ax.set_title(
        "Evolución del precio de la canasta familiar en el Eje Cafetero\n"
        f"Índice base 100 = {base_period.strftime('%b %Y')}",
        fontsize=13,
        fontweight="bold",
    )
    ax.set_xlabel("Período")
    ax.set_ylabel(f"Índice de precios (base {base_period.strftime('%b %Y')} = 100)")

    output_path = output_dir / "01_indice_precios_evolucion.png"
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return output_path


def build_city_price_index(
    data: pd.DataFrame,
    city_column: str = "Ciudad",
    price_column: str = "Precio_medio",
    product_column: str = "Productos",
) -> tuple[pd.Series, int]:
    """Builds a price-level index per city over a comparable basket.

    Only products present in every city are kept, so the comparison is not
    biased by each city sampling a different product mix. Each product is
    normalized against its cross-city mean price; the median of those
    relatives per city is a robust price-level index where 100 = average.
    """
    df = data.copy()

    n_cities = df[city_column].nunique()
    products_per_city = df.groupby(product_column)[city_column].nunique()
    common_products = products_per_city[products_per_city == n_cities].index

    comparable = df[df[product_column].isin(common_products)]
    by_product_city = (
        comparable.groupby([product_column, city_column])[price_column]
        .mean()
        .reset_index()
    )
    product_mean = by_product_city.groupby(product_column)[price_column].transform("mean")
    by_product_city["price_relative"] = (
        by_product_city[price_column] / product_mean * 100
    )

    index_series = (
        by_product_city.groupby(city_column)["price_relative"]
        .median()
        .sort_values()
        .rename("indice")
    )

    return index_series, len(common_products)


def plot_city_price_index(
    index_series: pd.Series,
    n_products: int,
    output_dir: Path = FIGURES_DIR,
) -> Path:
    """Plots the per-city price-level index as a horizontal bar chart."""
    output_dir.mkdir(parents=True, exist_ok=True)

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))

    # red = above average (more expensive), blue = below average (cheaper)
    colors = ["#c0392b" if value >= 100 else "#1f4e79" for value in index_series.values]
    bars = ax.barh(index_series.index, index_series.values, color=colors)
    ax.axvline(100, color="grey", linestyle="--", linewidth=1.2)

    for bar, value in zip(bars, index_series.values):
        ax.annotate(
            f"{value:.1f}",
            xy=(value, bar.get_y() + bar.get_height() / 2),
            xytext=(5, 0),
            textcoords="offset points",
            va="center",
            fontweight="bold",
        )

    # zoom around 100 so the differences between cities are readable
    low = min(index_series.min(), 100) - 2
    high = max(index_series.max(), 100) + 2
    ax.set_xlim(low, high)

    ax.set_title(
        "Nivel de precios por ciudad en el Eje Cafetero\n"
        f"Canasta comparable de {n_products} productos (100 = promedio entre ciudades)",
        fontsize=13,
        fontweight="bold",
    )
    ax.set_xlabel("Índice de nivel de precios (100 = promedio entre ciudades)")
    ax.set_ylabel("Ciudad")

    output_path = output_dir / "02_indice_precios_ciudad.png"
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return output_path

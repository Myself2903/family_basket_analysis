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

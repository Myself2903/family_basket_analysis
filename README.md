# Family Basket Analysis

This is a project that analyzes the prices of family basket products in four cities from the Eje Cafetero (Colombia) during the period 2022 - 2025 using Python. The dataset can be found [here](https://www.datos.gov.co/Agricultura-y-Desarrollo-Rural/Historico-de-Precios-Productos-de-la-Canasta-Famil/gdqq-rry2/about_data).

## 🎥 Presentation Video

Watch the project presentation here: [Presentation Video](https://universidadmag-my.sharepoint.com/:v:/g/personal/yirleidismarquezac_unimagdalena_edu_co/IQDtLAQsI03yTpEiXNFtj995ASehMLOpv5CvUrZ1ZQemAuI?e=M52PkY)

## Usage
You can run the project via pip or uv.

#### Run using pip
If you are using pip its highly recommended to make use of virtual environments:
```
python -m venv .venv
```
Activate it depending on your system:
```
# For windows
.venv\Scripts\activate
```
```
# For MacOS and linux
source .venv/bin/activate
```
And then resolve the dependencies and run the project: 
```
pip install .
python main.py
```

#### Run using uv
UV will manage virtual environments for you, so all you need to do is:
```
uv run main.py
```
## Output

The analysis generates three plots under the `figures/` directory:

1. **Price Index Evolution** – Tracks the evolution of a price index over time.
2. **City Price Comparison** – Compares the price index across cities.
3. **Category Volatility** – Shows price variability across product categories.

Generated figures are saved as PNG files.

## CLI Options

The application supports the following optional arguments:

| Flag | Description |
|--------|-------------|
| `-v`, `--verbose` | Enables verbose mode. Displays detailed information about the dataset, including structure, descriptive statistics, categorical value distributions, and generated feature summaries. |

### Examples

Run the project normally:

```bash
python main.py
```

Run the project with detailed output:

```bash
python main.py --verbose
```

or

```bash
python main.py -v
```

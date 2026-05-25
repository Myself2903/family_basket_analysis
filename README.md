# Family Basket Analysis

This is a project that analyzes the prices of family basket products in four cities from the Eje Cafetero (Colombia) during the period 2022 - 2025 using Python. The dataset can be found [here](https://www.datos.gov.co/Agricultura-y-Desarrollo-Rural/Historico-de-Precios-Productos-de-la-Canasta-Famil/gdqq-rry2/about_data).

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

from pathlib import Path

FILE_PATH = Path("data/Historico_de_Precios_Productos_de_la_Canasta_Familiar_RAP_Eje_Cafetero_20260525.csv")

FIGURES_DIR = Path("figures")

NUMERIC_COLUMNS = [
    "Precio_mínimo",
    "Precio_máximo",
    "Precio_medio",
]

DATE_COLUMNS = ["Fecha_inicial", "Fecha_final"]

MONTHS_MAPPING = {
    'enero': '01',
    'febrero': '02',
    'marzo': '03',
    'abril': '04',
    'mayo': '05',
    'junio': '06',
    'julio': '07',
    'agosto': '08',
    'septiembre': '09',
    'octubre': '10',
    'noviembre': '11',
    'diciembre': '12'
}

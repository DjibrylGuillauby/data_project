# src/utils/data_loader.py
import os
import pandas as pd

from config import CACHE_TTL_SECONDS, CLEAN_PATH
from src.utils.get_data import get_data
from src.utils.clean_data import clean_data
from src.utils.common_functions import is_cache_valid


def load_current_countries_data() -> pd.DataFrame:
    """
    Charge les données 'current' depuis data/cleaned si le cache est valide.
    Sinon, rafraîchit en appelant get_data() puis clean_data().
    """
    if is_cache_valid(CLEAN_PATH, CACHE_TTL_SECONDS):
        return pd.read_csv(CLEAN_PATH)

    # Rafraîchissement
    get_data()
    clean_data()
    return pd.read_csv(CLEAN_PATH)


def load_historical_year_data(year: int) -> pd.DataFrame:
    """
    Cache disque par année pour éviter de re-taper l'API à chaque changement.
    On stocke dans data/cleaned/historical_<year>.csv
    """
    hist_path = os.path.join("data", "cleaned", f"historical_{year}.csv")

    if is_cache_valid(hist_path, CACHE_TTL_SECONDS):
        return pd.read_csv(hist_path)

    # Import local pour éviter import circulaire si tu bouges la fonction plus tard
    from src.utils.historical import fetch_historical_countries

    df = fetch_historical_countries(year)
    os.makedirs(os.path.dirname(hist_path), exist_ok=True)
    df.to_csv(hist_path, index=False, encoding="utf-8")  # écrit le cache [web:97]
    return df

# src/utils/clean_data.py
import json
import os
import pandas as pd

RAW_PATH = os.path.join("data", "raw", "rawdata.json")
CLEAN_PATH = os.path.join("data", "cleaned", "cleaneddata.csv")
RAW_PATH_CONTINENTS = os.path.join("data", "raw", "rawdata_continents.json")
CLEAN_PATH_CONTINENTS = os.path.join("data", "cleaned", "cleaneddata_continents.csv")
CLEAN_PATH_COUNTRY_CONTINENT = os.path.join("data", "cleaned", "country_continent.csv")

KEEP_COLS = [
    "country", "cases", "deaths", "recovered", "active", "critical",
    "casesPerOneMillion", "population", "todayCases", "todayDeaths"
]

KEEP_COLS_C = [
    "continent", "cases", "deaths", "recovered", "active"
]

def clean_data():
    os.makedirs(os.path.dirname(CLEAN_PATH), exist_ok=True)

    with open(RAW_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # Extraire iso3/lat/long depuis countryInfo
    df["iso3"] = df["countryInfo"].apply(lambda x: x.get("iso3") if isinstance(x, dict) else None)
    df["lat"] = df["countryInfo"].apply(lambda x: x.get("lat") if isinstance(x, dict) else None)
    df["long"] = df["countryInfo"].apply(lambda x: x.get("long") if isinstance(x, dict) else None)

    df = df[["country", "iso3", "lat", "long"] + KEEP_COLS[1:]]  # country déjà inclus
    df = df[df["iso3"].notna()]  # indispensable pour la carte choropleth

    # Types numériques (sécurise l’histogramme)
    num_cols = [c for c in df.columns if c not in ["country", "iso3"]]
    df[num_cols] = df[num_cols].apply(pd.to_numeric, errors="coerce").fillna(0)

    df.to_csv(CLEAN_PATH, index=False, encoding="utf-8")
    return CLEAN_PATH

def clean_data_continents():
    os.makedirs(os.path.dirname(CLEAN_PATH_CONTINENTS), exist_ok=True)

    with open(RAW_PATH_CONTINENTS, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    df = df[KEEP_COLS_C] 
    df.to_csv(CLEAN_PATH_CONTINENTS, index=False, encoding="utf-8")
    return CLEAN_PATH_CONTINENTS

def get_country_continent_csv():
    """
    Construit un CSV pays–continent à partir de rawdata_continents.json
    """
    os.makedirs(os.path.dirname(CLEAN_PATH_COUNTRY_CONTINENT), exist_ok=True)

    with open(RAW_PATH_CONTINENTS, "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    for continent in data:
        continent_name = continent["continent"]
        for country in continent["countries"]:
            rows.append({
                "country": country,
                "continent": continent_name
            })

    df = pd.DataFrame(rows)
    df = df.drop_duplicates().sort_values("country")

    df.to_csv(CLEAN_PATH_COUNTRY_CONTINENT,index=False,encoding="utf-8")

    return CLEAN_PATH_COUNTRY_CONTINENT

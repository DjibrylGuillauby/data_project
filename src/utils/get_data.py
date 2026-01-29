# src/utils/get_data.py
import json
import os
import requests

RAW_PATH = os.path.join("data", "raw", "rawdata.json")
URL = "https://disease.sh/v3/covid-19/countries"
RAW_PATH_CONTINENTS = os.path.join("data", "raw", "rawdata_continents.json")
URL_c = "https://disease.sh/v3/covid-19/continents?strict=true"

def get_data():
    os.makedirs(os.path.dirname(RAW_PATH), exist_ok=True)
    r = requests.get(URL, timeout=15)
    r.raise_for_status()
    data = r.json()

    with open(RAW_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    return RAW_PATH

def get_data_continents():

    os.makedirs(os.path.dirname(RAW_PATH_CONTINENTS), exist_ok=True)
    r = requests.get(URL_c, timeout=15)
    r.raise_for_status()
    data = r.json()

    with open(RAW_PATH_CONTINENTS, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    return RAW_PATH_CONTINENTS
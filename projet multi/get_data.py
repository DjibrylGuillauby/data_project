import requests
import csv
import os

# Chemin du dossier
output_dir = "data/raw"
os.makedirs(output_dir, exist_ok=True)  # crée le dossier s'il n'existe pas


list_url = []
list_csv = []

# Choix des URL et nom de fichiers

# Country
list_url.append("https://disease.sh/v3/covid-19/countries")
list_csv.append(os.path.join(output_dir, "countries_data.csv"))

# Par année
list_url.append("https://disease.sh/v3/covid-19/historical?lastdays=all")
list_csv.append(os.path.join(output_dir, "historical_data.csv"))

for i in range(len(list_url)):
    response = requests.get(list_url[i])
    data = response.json()   # ici data c'est une liste d'objets [{...}, {...}, ...]

    first_item = data[0]

    with open(list_csv[i], "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(first_item.keys())
        for item in data:
            writer.writerow(item.values())


import requests
import csv

url = "https://disease.sh/v3/covid-19/countries"
response = requests.get(url)
data = response.json()   # ici data c'est une liste d'objets [{...}, {...}, ...]

csv_filename = "api_data.csv"
first_item = data[0]

with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(first_item.keys())
    for item in data:
        writer.writerow(item.values())

print(f"CSV créé : {csv_filename}")

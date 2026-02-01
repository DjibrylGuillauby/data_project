import pandas as pd
import requests
import os
from src.utils.clean_data import get_country_continent_csv

def fetch_historical_countries(year):
    """Récupère les données historiques par pays pour une année donnée"""
    url = f"https://disease.sh/v3/covid-19/historical?lastdays=all"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        countries_data = []
        
        for country in data:
            country_name = country['country']
            timeline = country['timeline']
            
            # Chercher la date du 31 décembre de l'année
            target_date = f"12/31/{str(year)[2:]}"  # Format: MM/DD/YY
            
            # Chercher toutes les dates de décembre de cette année
            december_dates = [d for d in timeline['cases'].keys() if d.endswith(f"/{str(year)[2:]}") and d.startswith("12/")]
            
            if december_dates:
                # Prendre la dernière date disponible en décembre
                last_date = sorted(december_dates, key=lambda x: int(x.split('/')[1]))[-1]
                
                cases = timeline['cases'].get(last_date, 0)
                deaths = timeline['deaths'].get(last_date, 0)
                recovered = timeline['recovered'].get(last_date, 0)
                
                countries_data.append({
                    'country': country_name,
                    'cases': cases,
                    'deaths': deaths,
                    'recovered': recovered,
                    'active': cases - deaths - recovered
                })
        
        df = pd.DataFrame(countries_data)
        
        # Ajouter les codes ISO3
        iso_mapping = {
            'USA': 'USA', 'India': 'IND', 'Brazil': 'BRA', 'France': 'FRA',
            'Germany': 'DEU', 'UK': 'GBR', 'Italy': 'ITA', 'Russia': 'RUS',
            'Turkey': 'TUR', 'Spain': 'ESP', 'Vietnam': 'VNM', 'Argentina': 'ARG',
            'Japan': 'JPN', 'Netherlands': 'NLD', 'Iran': 'IRN', 'Colombia': 'COL',
            'Indonesia': 'IDN', 'Poland': 'POL', 'Mexico': 'MEX', 'Ukraine': 'UKR',
            'South Africa': 'ZAF', 'Philippines': 'PHL', 'Malaysia': 'MYS',
            'Peru': 'PER', 'Canada': 'CAN', 'Czechia': 'CZE', 'Belgium': 'BEL',
            'Thailand': 'THA', 'Israel': 'ISR', 'Portugal': 'PRT', 'Greece': 'GRC',
            'Chile': 'CHL', 'Denmark': 'DNK', 'Romania': 'ROU', 'Sweden': 'SWE',
            'Iraq': 'IRQ', 'Switzerland': 'CHE', 'Bangladesh': 'BGD',
            'Pakistan': 'PAK', 'South Korea': 'KOR', 'Austria': 'AUT',
            'Serbia': 'SRB', 'Hungary': 'HUN', 'Jordan': 'JOR', 'Morocco': 'MAR',
            'Nepal': 'NPL', 'UAE': 'ARE', 'Cuba': 'CUB', 'Lebanon': 'LBN',
            'Saudi Arabia': 'SAU', 'Kazakhstan': 'KAZ', 'Tunisia': 'TUN',
            'Guatemala': 'GTM', 'Bulgaria': 'BGR', 'Ecuador': 'ECU',
            'Bolivia': 'BOL', 'Slovakia': 'SVK', 'Azerbaijan': 'AZE',
            'Croatia': 'HRV', 'Costa Rica': 'CRI', 'Myanmar': 'MMR',
            'Lithuania': 'LTU', 'Slovenia': 'SVN', 'Belarus': 'BLR',
            'Uruguay': 'URY', 'Panama': 'PAN', 'Mongolia': 'MNG',
            'Paraguay': 'PRY', 'Sri Lanka': 'LKA', 'Kenya': 'KEN',
            'Kuwait': 'KWT', 'Dominican Republic': 'DOM', 'Palestine': 'PSE',
            'Georgia': 'GEO', 'Ethiopia': 'ETH', 'Venezuela': 'VEN',
            'Egypt': 'EGY', 'Moldova': 'MDA', 'Libya': 'LBY',
            'Honduras': 'HND', 'Armenia': 'ARM', 'Bosnia': 'BIH',
            'Oman': 'OMN', 'Qatar': 'QAT', 'Zambia': 'ZMB',
            'Albania': 'ALB', 'North Macedonia': 'MKD', 'Algeria': 'DZA',
            'Botswana': 'BWA', 'Nigeria': 'NGA', 'Zimbabwe': 'ZWE',
            'Uzbekistan': 'UZB', 'Montenegro': 'MNE', 'Mozambique': 'MOZ',
            'Finland': 'FIN', 'Latvia': 'LVA', 'Kyrgyzstan': 'KGZ',
            'Norway': 'NOR', 'Singapore': 'SGP', 'Ireland': 'IRL',
            'El Salvador': 'SLV', 'China': 'CHN', 'Australia': 'AUS',
            'Afghanistan': 'AFG', 'Cameroon': 'CMR', 'Namibia': 'NAM',
            'Uganda': 'UGA', 'Cyprus': 'CYP', 'Ghana': 'GHA',
            'Rwanda': 'RWA', 'Jamaica': 'JAM', 'Cambodia': 'KHM',
            'Trinidad and Tobago': 'TTO', 'Estonia': 'EST', 'Senegal': 'SEN',
            'Malawi': 'MWI', 'Ivory Coast': 'CIV', 'DRC': 'COD',
            'Suriname': 'SUR', 'Maldives': 'MDV', 'Syria': 'SYR',
            'Laos': 'LAO', 'Mauritania': 'MRT', 'Fiji': 'FJI',
            'Guyana': 'GUY', 'Mauritius': 'MUS', 'Eswatini': 'SWZ',
            'Bhutan': 'BTN', 'Luxembourg': 'LUX', 'Madagascar': 'MDG',
            'Sudan': 'SDN', 'Malta': 'MLT', 'Cabo Verde': 'CPV',
            'Bahamas': 'BHS', 'Belize': 'BLZ', 'Iceland': 'ISL',
            'Hong Kong': 'HKG', 'Barbados': 'BRB', 'S. Korea': 'KOR',
            'Taiwan': 'TWN', 'New Zealand': 'NZL', 'Nicaragua': 'NIC'
        }
        
        df['iso3'] = df['country'].map(iso_mapping)
        df = df[df['iso3'].notna()]
        
        return df
        
    except Exception as e:
        print(f"Erreur données historiques: {e}")
        return pd.DataFrame()

def fetch_historical_continents(year):
    hist_path = os.path.join("data", "cleaned", f"historical_{year}.csv")

    if os.path.exists(hist_path):
        df_countries = pd.read_csv(hist_path)
    else:
        df_countries = fetch_historical_countries(year)
        df_countries.to_csv(hist_path, index=False, encoding="utf-8")

    if df_countries.empty:
        return pd.DataFrame()

    mapping_path = os.path.join("data", "cleaned", "country_continent.csv")
    if not os.path.exists(mapping_path):
        get_country_continent_csv()
    df_mapping = pd.read_csv(mapping_path)

    df_countries = df_countries.merge(
        df_mapping,
        on="country",
        how="left"
    )

    df_countries = df_countries[df_countries["continent"].notna()]

    df_continent = (
        df_countries
        .groupby("continent")[["cases", "deaths", "recovered", "active"]]
        .sum()
        .reset_index()
    )

    df_continent["year"] = year
    return df_continent


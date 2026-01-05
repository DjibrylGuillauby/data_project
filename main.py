# Importation des bibliothèques nécessaires
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
from datetime import datetime

# Configuration de l'application Dash
app = dash.Dash(__name__)
app.title = "COVID-19 Dashboard Mondial"

def fetch_countries_data():
    """Récupère les données COVID-19 actuelles par pays"""
    url = "https://disease.sh/v3/covid-19/countries"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Création du DataFrame
        df = pd.DataFrame(data)
        
        # Extraction des informations nécessaires
        df['iso3'] = df['countryInfo'].apply(lambda x: x.get('iso3', None))
        df['lat'] = df['countryInfo'].apply(lambda x: x.get('lat', None))
        df['long'] = df['countryInfo'].apply(lambda x: x.get('long', None))
        
        # Sélection des colonnes
        df = df[['country', 'iso3', 'cases', 'deaths', 'recovered', 
                 'active', 'critical', 'casesPerOneMillion', 'population',
                 'todayCases', 'todayDeaths', 'lat', 'long']]
        
        return df
        
    except Exception as e:
        print(f"Erreur pays: {e}")
        return pd.DataFrame()

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

# Récupération des données actuelles
print("Chargement des données...")
df_countries = fetch_countries_data()
print(f"Données chargées: {len(df_countries)} pays")

# Layout de l'application
app.layout = html.Div([
    html.Div([
        html.H1("Dashboard COVID-19 mondial",
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),
        
        # Sélecteurs
        html.Div([
            html.Div([
                html.Label("Sélectionner l'année :",
                          style={'fontWeight': 'bold', 'fontSize': 16, 'marginBottom': 10}),
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[
                        {'label': 'Année 2020', 'value': 2020},
                        {'label': 'Année 2021', 'value': 2021},
                        {'label': 'Année 2022', 'value': 2022},
                        {'label': 'Année 2023', 'value': 2023},
                        {'label': 'Données actuelles', 'value': 'all'}
                    ],
                    value='all',
                    style={'width': '100%'}
                )
            ], style={'width': '30%', 'display': 'inline-block', 'paddingRight': '20px'}),
            
            html.Div([
                html.Label("Métrique à afficher :", 
                          style={'fontWeight': 'bold', 'fontSize': 16, 'marginBottom': 10}),
                dcc.Dropdown(
                    id='metric-dropdown',
                    options=[
                        {'label': 'Cas totaux', 'value': 'cases'},
                        {'label': 'Décès totaux', 'value': 'deaths'},
                        {'label': 'Rétablis', 'value': 'recovered'},
                        {'label': 'Cas actifs', 'value': 'active'}
                    ],
                    value='cases',
                    style={'width': '100%'}
                )
            ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'})
        ], style={'textAlign': 'center', 'marginBottom': 40}),
        
        # Statistiques globales
        html.Div(id='global-stats', style={'textAlign': 'center', 'marginBottom': 30}),
        
        # Carte géolocalisée
        html.Div([
            html.H2("Carte mondiale des cas", style={'textAlign': 'center'}),
            html.P(id='map-date-info', style={'textAlign': 'center', 'fontSize': 14, 'color': '#7f8c8d', 'marginBottom': 20}),
            dcc.Graph(id='world-map', style={'height': '600px'}, config={'displaylogo': False})
        ], style={'marginBottom': 40}),
        
        # Histogramme
        html.Div([
            html.H2("Top 20 des pays les plus touchés", style={'textAlign': 'center'}),
            dcc.Graph(id='top-countries-bar', style={'height': '500px'})
        ])
    ], style={'padding': '20px', 'fontFamily': 'Arial, sans-serif', 'maxWidth': '1400px', 'margin': 'auto'})
])

# Callback pour les statistiques globales
@app.callback(
    Output('global-stats', 'children'),
    [Input('year-dropdown', 'value'),
     Input('metric-dropdown', 'value')]
)
def update_stats(selected_year, selected_metric):
    """Met à jour les statistiques globales"""
    
    # Charger les données selon l'année
    if selected_year == 'all':
        df = df_countries
    else:
        df = fetch_historical_countries(selected_year)
    
    if df.empty:
        return html.Div("Aucune donnée disponible")
    
    total_cases = int(df['cases'].sum())
    total_deaths = int(df['deaths'].sum())
    total_recovered = int(df['recovered'].sum())
    total_active = int(df['active'].sum())
    
    return html.Div([
        html.Div([
            html.Div([
                html.H3(f"{total_cases:,}", style={'color': '#3498db', 'margin': 0}),
                html.P("Cas totaux", style={'margin': 0, 'fontSize': 14})
            ], style={'display': 'inline-block', 'margin': '0 30px', 'verticalAlign': 'top'}),
            
            html.Div([
                html.H3(f"{total_deaths:,}", style={'color': '#e74c3c', 'margin': 0}),
                html.P("Décès", style={'margin': 0, 'fontSize': 14})
            ], style={'display': 'inline-block', 'margin': '0 30px', 'verticalAlign': 'top'}),
            
            html.Div([
                html.H3(f"{total_recovered:,}", style={'color': '#2ecc71', 'margin': 0}),
                html.P("Rétablis", style={'margin': 0, 'fontSize': 14})
            ], style={'display': 'inline-block', 'margin': '0 30px', 'verticalAlign': 'top'}),
            
            html.Div([
                html.H3(f"{total_active:,}", style={'color': '#f39c12', 'margin': 0}),
                html.P("Cas actifs", style={'margin': 0, 'fontSize': 14})
            ], style={'display': 'inline-block', 'margin': '0 30px', 'verticalAlign': 'top'})
        ], style={'padding': '25px', 'backgroundColor': '#ecf0f1', 'borderRadius': '10px', 
                  'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
    ])

# Callback pour la carte mondiale
@app.callback(
    [Output('world-map', 'figure'),
     Output('map-date-info', 'children')],
    [Input('year-dropdown', 'value'),
     Input('metric-dropdown', 'value')]
)
def update_world_map(selected_year, selected_metric):
    """Crée une carte choroplèthe du monde avec les données COVID-19"""
    
    # Charger les données selon l'année
    if selected_year == 'all':
        df = df_countries
        date_text = "Données actuelles (dernières disponibles)"
    else:
        df = fetch_historical_countries(selected_year)
        date_text = f"Données au 31 décembre {selected_year}"
    
    if df.empty:
        return go.Figure(), "Aucune donnée disponible pour cette période"
    
    metric_info = {
        'cases': {'title': 'Cas totaux', 'color': 'Blues'},
        'deaths': {'title': 'Décès totaux', 'color': 'Reds'},
        'recovered': {'title': 'Rétablis', 'color': 'Greens'},
        'active': {'title': 'Cas actifs', 'color': 'Oranges'}
    }
    
    info = metric_info.get(selected_metric, metric_info['cases'])
    
    fig = px.choropleth(
        df,
        locations="iso3",
        color=selected_metric,
        hover_name="country",
        hover_data={
            'cases': ':,',
            'deaths': ':,',
            'recovered': ':,',
            'active': ':,',
            'iso3': False
        },
        color_continuous_scale=info['color'],
        labels={selected_metric: info['title']}
    )
    
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth',
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        paper_bgcolor='white'
    )
    
    return fig, date_text

# Callback pour l'histogramme
@app.callback(
    Output('top-countries-bar', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('metric-dropdown', 'value')]
)
def update_bar_chart(selected_year, selected_metric):
    """Crée un histogramme des 20 pays les plus touchés"""
    
    # Charger les données selon l'année
    if selected_year == 'all':
        df = df_countries
    else:
        df = fetch_historical_countries(selected_year)
    
    if df.empty:
        return go.Figure()
    
    metric_info = {
        'cases': {'title': 'Cas totaux', 'color': '#3498db'},
        'deaths': {'title': 'Décès totaux', 'color': '#e74c3c'},
        'recovered': {'title': 'Rétablis', 'color': '#2ecc71'},
        'active': {'title': 'Cas actifs', 'color': '#f39c12'}
    }
    
    info = metric_info.get(selected_metric, metric_info['cases'])
    
    df_top = df.nlargest(20, selected_metric).sort_values(selected_metric)
    
    fig = go.Figure(data=[
        go.Bar(
            x=df_top[selected_metric],
            y=df_top['country'],
            orientation='h',
            marker=dict(
                color=df_top[selected_metric],
                colorscale=[[0, '#f0f0f0'], [1, info['color']]],
                line=dict(color=info['color'], width=1)
            ),
            text=df_top[selected_metric].apply(lambda x: f"{x:,}"),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>' + 
                         info['title'] + ': %{x:,}<extra></extra>'
        )
    ])
    
    year_text = f" - {selected_year}" if selected_year != 'all' else " - Actuelles"
    
    fig.update_layout(
        title={
            'text': f"Top 20 - {info['title']}{year_text}",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        xaxis_title=info['title'],
        yaxis_title="",
        showlegend=False,
        height=500,
        margin=dict(l=150, r=80, t=60, b=50),
        plot_bgcolor='white',
        xaxis=dict(gridcolor='#e0e0e0'),
        paper_bgcolor='white'
    )
    
    return fig

# Lancement de l'application
if __name__ == '__main__':
    print("\n" + "="*60)
    print("Dashboard COVID-19 démarré !")
    print("Ouvrez votre navigateur: http://localhost:8050")
    print("="*60 + "\n")
    app.run(debug=True, port=8050)

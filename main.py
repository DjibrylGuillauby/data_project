# main.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

from src.utils.data_loader import load_current_countries_data, load_historical_year_data

# Charge une seule fois au démarrage (via cache TTL)
df_countries = load_current_countries_data()

app = dash.Dash(__name__)
app.title = "COVID-19 Dashboard mondial"

app.layout = html.Div([
    html.Div([
        html.H1("Dashboard COVID-19 mondial",
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),

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

        html.Div(id='global-stats', style={'textAlign': 'center', 'marginBottom': 30}),

        html.Div([
            html.H2("Carte mondiale des cas", style={'textAlign': 'center'}),
            html.P(id='map-date-info',
                   style={'textAlign': 'center', 'fontSize': 14, 'color': '#7f8c8d', 'marginBottom': 20}),
            dcc.Graph(id='world-map', style={'height': '600px'}, config={'displaylogo': False})
        ], style={'marginBottom': 40}),

        html.Div([
            html.H2("Top 20 des pays les plus touchés", style={'textAlign': 'center'}),
            dcc.Graph(id='top-countries-bar', style={'height': '500px'})
        ])
    ], style={'padding': '20px', 'fontFamily': 'Arial, sans-serif', 'maxWidth': '1400px', 'margin': 'auto'})
])

def _get_df_for_year(selected_year):
    if selected_year == 'all':
        return df_countries
    return load_historical_year_data(int(selected_year))

@app.callback(
    Output('global-stats', 'children'),
    [Input('year-dropdown', 'value'),
     Input('metric-dropdown', 'value')]
)
def update_stats(selected_year, selected_metric):
    df = _get_df_for_year(selected_year)
    if df.empty:
        return html.Div("Aucune donnée disponible")

    total_cases = int(df['cases'].sum())
    total_deaths = int(df['deaths'].sum())
    total_recovered = int(df['recovered'].sum())
    total_active = int(df['active'].sum())

    return html.Div([
        html.Div([
            html.Div([html.H3(f"{total_cases:,}", style={'color': '#3498db', 'margin': 0}),
                      html.P("Cas totaux", style={'margin': 0, 'fontSize': 14})],
                     style={'display': 'inline-block', 'margin': '0 30px', 'verticalAlign': 'top'}),
            html.Div([html.H3(f"{total_deaths:,}", style={'color': '#e74c3c', 'margin': 0}),
                      html.P("Décès", style={'margin': 0, 'fontSize': 14})],
                     style={'display': 'inline-block', 'margin': '0 30px', 'verticalAlign': 'top'}),
            html.Div([html.H3(f"{total_recovered:,}", style={'color': '#2ecc71', 'margin': 0}),
                      html.P("Rétablis", style={'margin': 0, 'fontSize': 14})],
                     style={'display': 'inline-block', 'margin': '0 30px', 'verticalAlign': 'top'}),
            html.Div([html.H3(f"{total_active:,}", style={'color': '#f39c12', 'margin': 0}),
                      html.P("Cas actifs", style={'margin': 0, 'fontSize': 14})],
                     style={'display': 'inline-block', 'margin': '0 30px', 'verticalAlign': 'top'})
        ], style={'padding': '25px', 'backgroundColor': '#ecf0f1', 'borderRadius': '10px',
                  'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
    ])

@app.callback(
    [Output('world-map', 'figure'),
     Output('map-date-info', 'children')],
    [Input('year-dropdown', 'value'),
     Input('metric-dropdown', 'value')]
)
def update_world_map(selected_year, selected_metric):
    df = _get_df_for_year(selected_year)
    date_text = "Données actuelles (dernières disponibles)" if selected_year == 'all' else f"Données au 31 décembre {selected_year}"

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
        hover_data={'cases': ':,', 'deaths': ':,', 'recovered': ':,', 'active': ':,', 'iso3': False},
        color_continuous_scale=info['color'],
        labels={selected_metric: info['title']}
    )
    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth', bgcolor='rgba(0,0,0,0)'),
        margin=dict(l=0, r=0, t=30, b=0),
        paper_bgcolor='white'
    )
    return fig, date_text

@app.callback(
    Output('top-countries-bar', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('metric-dropdown', 'value')]
)
def update_bar_chart(selected_year, selected_metric):
    df = _get_df_for_year(selected_year)
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
            marker=dict(color=df_top[selected_metric],
                        colorscale=[[0, '#f0f0f0'], [1, info['color']]],
                        line=dict(color=info['color'], width=1)),
            text=df_top[selected_metric].apply(lambda x: f"{x:,}"),
            textposition='outside'
        )
    ])

    year_text = f" - {selected_year}" if selected_year != 'all' else " - Actuelles"
    fig.update_layout(
        title={'text': f"Top 20 - {info['title']}{year_text}", 'x': 0.5, 'xanchor': 'center', 'font': {'size': 20}},
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

if __name__ == '__main__':
    app.run(debug=True, port=8050, use_reloader=False)

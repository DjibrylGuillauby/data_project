import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('api_data.csv')

# Sélectionner 10 pays au hasard
sample_df = df.sample(10)

# Création de la figure
fig = go.Figure(
    data = [
        go.Bar(
            x = sample_df["country"],
            y = sample_df["casesPerOneMillion"],
            text = sample_df["casesPerOneMillion"],
            textposition="auto"
        )
    ]
)

# Mise en forme
fig.update_layout(
    title="Nombre de cas pour 1 millions pour 10 pays pris au hasard",
    xaxis_title="Pays",
    yaxis_title="Nombre de cas",
     yaxis=dict(range=[0, 1_000_000]),
    template="plotly_white"
)

# Affichage
fig.show()
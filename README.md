# Dashboard COVID-19

## User Guide

### Prérequis

- Python
- pip

### Installation

Cloner le dépôt puis installer les dépendances :

- Commande pour cloner le dépôt : ``git clone https://github.com/DjibrylGuillauby/data_project.git``
- Commande pour installer les dépendances : ``python -m pip install -r requirements.txt``

### Lancement

Le programme doit être exécuté avec la commande : ``python main.py``

## Data

Nous avons décidé de prendre un jeux de données sur le covid 19 : ``https://disease.sh/``.
Les données ont pour source Worldometers et sont mise à jour toutes les 10 minutes.
Nous avons plus précisément utilisé :

_Nous trions les données afin d'avoir le nombre de cas, de morts, de soignés et de cas actifs selon la période et la zone géographique_

- ``https://disease.sh/v3/covid-19/countries`` pour chaque pays à l'état actuel
- ``https://disease.sh/v3/covid-19/historical?lastdays=all``pour chaque pays puis chaque continent selon l'année choisi (2020, 2021 ou 2022)
- ``https://disease.sh/v3/covid-19/historical?lastdays=all`` pour chaque continent à l'état actuel

## Developer Guide

## Rapport d’analyse

### Évolution globale de la pandémie (2020–2022)

L’analyse temporelle met en évidence plusieurs phases distinctes de la pandémie :

2020 correspond à la phase initiale de propagation rapide du virus, marquée par une croissance exponentielle du nombre de cas.\
2021 constitue l’année la plus critique en termes de volume, avec des pics importants de contaminations et de décès, liés notamment à l’émergence de nouveaux variants.\
2022 montre une relative stabilisation de la situation sanitaire, caractérisée par une diminution du taux de mortalité malgré des vagues de contamination encore présentes.

Conclusion principale :
Bien que le nombre cumulé de cas continue d’augmenter au fil du temps, la proportion de décès par rapport aux cas confirmés diminue progressivement, suggérant une amélioration de la prise en charge médicale et l’impact des campagnes de vaccination.

### Analyse géographique par pays et par continent

La comparaison des données par zone géographique révèle des disparités significatives :

L’Europe et l’Amérique du Nord figurent parmi les régions les plus touchées en nombre total de cas.
Certains pays présentent un nombre élevé de cas mais un taux de mortalité relativement faible, tandis que d’autres affichent un impact plus sévère malgré une population moindre.\
Les continents ne sont pas affectés de manière homogène, ce qui reflète des différences en matière de systèmes de santé, de démographie et de politiques sanitaires.

Conclusion principale :
L’impact du COVID-19 varie fortement selon les régions du monde, mettant en évidence des inégalités structurelles et des réponses sanitaires hétérogènes face à la pandémie.

### Cas actifs, guérisons et décès

L’étude des indicateurs clés montre que :

Les cas actifs augmentent fortement lors des vagues épidémiques, avant de diminuer progressivement.\
Le nombre de personnes guéries croît de manière significative après chaque pic, dépassant largement les cas actifs sur le long terme.\
Les décès évoluent de façon plus linéaire, avec une croissance moins brutale que celle des cas confirmés.

Conclusion principale :
Malgré les périodes de forte pression sanitaire, la proportion de guérisons reste élevée, traduisant une capacité d’adaptation des systèmes de santé à l’échelle mondiale.

### Analyse annuelle comparative

La segmentation par année permet de dégager des profils distincts :

2020 : forte incertitude et croissance rapide des indicateurs.\
2021 : intensification de la pandémie avec les valeurs les plus élevées observées.\
2022 : diminution de la gravité globale, bien que le virus demeure présent.

Conclusion principale :
Chaque année présente des caractéristiques propres, illustrant l’évolution de la pandémie et l’adaptation progressive des réponses sanitaires internationales.

### Apport du dashboard

Ce dashboard constitue un outil d’aide à l’analyse permettant d’explorer l’évolution du COVID-19 à différentes échelles temporelles et géographiques, tout en facilitant l’identification des tendances clés de la pandémie.

## Copyright
import dash
from dash import Dash, dcc, html, dash_table, callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Symbol, Scheme
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import plotly.express as px

import pages.ranking as rk
import pages.evolution as evo
import pages.actors as actors
import pages.director as dr
import pages.studios as st
import pages.inclusivity as inclusivity
import pages.age as age
import pages.geo as geo

from data import tables



app = Dash(__name__)
server = app.server


tabs_styles = {
    'height': '44px'
}
tab_style = {
    'padding': '6px',
    'fontWeight': 'bold',
    'backgroundColor': '#171b26'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': 'rgb(31, 37, 54)',
    'color': 'white',
    'padding': '6px'
}

app.layout = html.Div(
    className="container scalable",
    children=[
        html.Div(
            id="banner",
            className="banner",
            children=[
                html.H6("BlockBuster Analysis"),
                html.Img(src="https://soyhuce.fr/content/uploads/2020/06/logo-soyhuce-blanc.png"),
            ],
        ),
        dcc.Tabs([
            dcc.Tab(label='Ranking By Film',children=[rk.layout()], style=tab_style,selected_style=tab_selected_style),
            dcc.Tab(label='Evolution', children=[evo.layout()], style=tab_style,selected_style=tab_selected_style),
            dcc.Tab(label='Actors success', children=[actors.layout()], style=tab_style,selected_style=tab_selected_style),
            dcc.Tab(label='Directors success', children=[dr.layout()], style=tab_style,selected_style=tab_selected_style),
            dcc.Tab(label='Studios success', children=[st.layout()], style=tab_style,selected_style=tab_selected_style),
            dcc.Tab(label='Gender Analysis', children=[inclusivity.layout()], style=tab_style,selected_style=tab_selected_style),
            dcc.Tab(label='Age Analysis', children=[age.layout()], style=tab_style,selected_style=tab_selected_style),
            dcc.Tab(label='Film Country Location', children=[geo.layout()], style=tab_style,selected_style=tab_selected_style)
        ], style=tabs_styles)
    ],
)



@app.callback(
    Output(component_id="actor-plot", component_property="figure"),
    Input(component_id="metric-select-actor", component_property="value"),
    Input(component_id="metric-select-actor-2", component_property="value"),
    Input(component_id="language-select-actor", component_property="value"),
    Input(component_id="director-select-actor", component_property="value"),
    Input(component_id="studio-select-actor", component_property="value"),
    Input(component_id="country-select-actor", component_property="value"),
    Input(component_id="date-select-actor", component_property="start_date"),
    Input(component_id="date-select-actor", component_property="end_date")
)
def update_table(metric,metric2, language, director, studio, country, start_date, end_date):

    df = tables['Actor'].merge(tables['Cast'], left_index=True, right_on='CastActorID').merge(tables['Film'], left_on='CastFilmID', right_index=True)

    if language != 'All':
        df = df[df['FilmLanguageID'] == language]

    if director != 'All':
        df = df[df['FilmDirectorID'] == director]

    if studio != 'All':
        df = df[df['FilmStudioID'] == studio]

    if country != 'All':
        df = df[df['FilmCountryID'] == country]

    df = df[df['FilmReleaseDate'].between(start_date, end_date)]
    
    if metric2 == "Average":
        data = df[['FilmBoxOfficeDollars', 'FilmBudgetDollars', 'FilmBenefits', 'ActorName']].groupby('ActorName').mean().sort_values(f"Film{metric}", ascending=False)
    elif metric2 == "Total":
        data = df[['FilmBoxOfficeDollars', 'FilmBudgetDollars', 'FilmBenefits', 'ActorName']].groupby('ActorName').sum().sort_values(f"Film{metric}", ascending=False)

    data = data.merge(df[['FilmName','ActorName']].groupby('ActorName').count(),left_index=True,right_index=True)
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(x=data.index, y=data[f"Film{metric}"].iloc[0:10],name=metric,offsetgroup=1), secondary_y=False)

    fig.add_trace(go.Bar(x=data.index, y=data[f"FilmName"].iloc[0:10],name='Number of Films',offsetgroup=2), secondary_y=True)

    fig.update_yaxes(tickprefix="$ ", ticksuffix="M ", secondary_y=False)

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#9fa6b7',title_text=f"Ranking of Actors with the best {metric} {metric2}",   
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
    )

    return fig

@app.callback(
    Output(component_id="director-plot", component_property="figure"),
    Input(component_id="metric-select-director", component_property="value"),
    Input(component_id="metric-select-director-2", component_property="value"),
    Input(component_id="language-select-director", component_property="value"),
    Input(component_id="director-select-director", component_property="value"),
    Input(component_id="studio-select-director", component_property="value"),
    Input(component_id="country-select-director", component_property="value"),
    Input(component_id="date-select-director", component_property="start_date"),
    Input(component_id="date-select-director", component_property="end_date")
)
def update_table(metric,metric2, language, director, studio, country, start_date, end_date):

    df = tables['Director'].merge(tables['Film'], right_on='FilmDirectorID', left_index=True)

    if language != 'All':
        df = df[df['FilmLanguageID'] == language]

    if director != 'All':
        df = df[df['FilmDirectorID'] == director]

    if studio != 'All':
        df = df[df['FilmStudioID'] == studio]

    if country != 'All':
        df = df[df['FilmCountryID'] == country]

    df = df[df['FilmReleaseDate'].between(start_date, end_date)]
    
    if metric2 == "Average":
        data = df[['FilmBoxOfficeDollars', 'FilmBudgetDollars', 'FilmBenefits', 'DirectorName']].groupby('DirectorName').mean().sort_values(f"Film{metric}", ascending=False)
    elif metric2 == "Total":
        data = df[['FilmBoxOfficeDollars', 'FilmBudgetDollars', 'FilmBenefits', 'DirectorName']].groupby('DirectorName').sum().sort_values(f"Film{metric}", ascending=False)

    data = data.merge(df[['FilmName','DirectorName']].groupby('DirectorName').count(),left_index=True,right_index=True)
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(x=data.index, y=data[f"Film{metric}"].iloc[0:10],name=metric,offsetgroup=1), secondary_y=False)

    fig.add_trace(go.Bar(x=data.index, y=data[f"FilmName"].iloc[0:10],name='Number of Films',offsetgroup=2), secondary_y=True)

    fig.update_yaxes(tickprefix="$ ", ticksuffix="M ", secondary_y=False)

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#9fa6b7',title_text=f"Ranking of Directors with the best {metric} {metric2}",   
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
    )

    return fig

@app.callback(
    Output(component_id="evolution-plot", component_property="figure"),
    Input(component_id="metric-select-evolution", component_property="value"),
    Input(component_id="language-select-evolution", component_property="value"),
    Input(component_id="director-select-evolution", component_property="value"),
    Input(component_id="studio-select-evolution", component_property="value"),
    Input(component_id="country-select-evolution", component_property="value"),
    Input(component_id="date-select-evolution", component_property="start_date"),
    Input(component_id="date-select-evolution", component_property="end_date")
)
def update_table(metric, language, director, studio, country, start_date, end_date):
    
    df = tables["Film"]

    if language != 'All':
        df = df[df['FilmLanguageID'] == language]

    if director != 'All':
        df = df[df['FilmDirectorID'] == director]

    if studio != 'All':
        df = df[df['FilmStudioID'] == studio]

    if country != 'All':
        df = df[df['FilmCountryID'] == country]

    df = df[df['FilmReleaseDate'].between(start_date, end_date)]

    if metric == "Average":
        data = df[['FilmBoxOfficeDollars', 'FilmBudgetDollars', 'FilmBenefits','FilmReleaseYear']].groupby('FilmReleaseYear').mean()
    if metric == "Total":
        data = df[['FilmBoxOfficeDollars', 'FilmBudgetDollars', 'FilmBenefits','FilmReleaseYear']].groupby('FilmReleaseYear').sum()
    
    data = data.merge(df[['FilmName','FilmReleaseYear']].groupby('FilmReleaseYear').count(), left_index=True, right_index=True)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    for i in ['FilmBoxOfficeDollars', 'FilmBudgetDollars', 'FilmBenefits']:
        fig.add_trace(go.Scatter(y=data[i], x=data.index, name=i), secondary_y=False)

    fig.add_trace(go.Scatter(y=data['FilmName'], x=data.index, name='Number of Films', line_color='white'), secondary_y=True)

    fig.update_yaxes(tickprefix="$ ", ticksuffix="M ", secondary_y=False)

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#9fa6b7',title_text=f"Global Box Offices/Budgets/Benefits {metric}")

    return fig

@app.callback(
    Output(component_id="studio-plot", component_property="figure"),
    Input(component_id="metric-select-studio", component_property="value"),
    Input(component_id="metric-select-studio-2", component_property="value"),
    Input(component_id="language-select-studio", component_property="value"),
    Input(component_id="director-select-studio", component_property="value"),
    Input(component_id="studio-select-studio", component_property="value"),
    Input(component_id="country-select-studio", component_property="value"),
    Input(component_id="date-select-studio", component_property="start_date"),
    Input(component_id="date-select-studio", component_property="end_date")
)
def update_table(metric,metric2, language, director, studio, country, start_date, end_date):

    df = tables['Studio'].merge(tables['Film'], right_on='FilmStudioID', left_index=True)

    if language != 'All':
        df = df[df['FilmLanguageID'] == language]

    if director != 'All':
        df = df[df['FilmDirectorID'] == director]

    if studio != 'All':
        df = df[df['FilmStudioID'] == studio]

    if country != 'All':
        df = df[df['FilmCountryID'] == country]

    df = df[df['FilmReleaseDate'].between(start_date, end_date)]
    
    if metric2 == "Average":
        data = df[['FilmBoxOfficeDollars', 'FilmBudgetDollars', 'FilmBenefits', 'StudioName']].groupby('StudioName').mean().sort_values(f"Film{metric}", ascending=False)
    elif metric2 == "Total":
        data = df[['FilmBoxOfficeDollars', 'FilmBudgetDollars', 'FilmBenefits', 'StudioName']].groupby('StudioName').sum().sort_values(f"Film{metric}", ascending=False)

    data = data.merge(df[['FilmName','StudioName']].groupby('StudioName').count(),left_index=True,right_index=True)
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(x=data.index, y=data[f"Film{metric}"].iloc[0:10],name=metric,offsetgroup=1), secondary_y=False)

    fig.add_trace(go.Bar(x=data.index, y=data[f"FilmName"].iloc[0:10],name='Number of Films',offsetgroup=2), secondary_y=True)

    fig.update_yaxes(tickprefix="$ ", ticksuffix="M ", secondary_y=False)

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#9fa6b7',title_text=f"Ranking of Studios with the best {metric} {metric2}",   
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
    )

    return fig

@app.callback(
    Output(component_id="inclusivity-plot-1", component_property="figure"),
    Input(component_id="metric-select-inclusivity", component_property="value"),
    Input(component_id="language-select-inclusivity", component_property="value"),
    Input(component_id="director-select-inclusivity", component_property="value"),
    Input(component_id="studio-select-inclusivity", component_property="value"),
    Input(component_id="country-select-inclusivity", component_property="value"),
    Input(component_id="date-select-inclusivity", component_property="start_date"),
    Input(component_id="date-select-inclusivity", component_property="end_date")
)
def update_table(metric, language, director, studio, country, start_date, end_date):
    
    if metric == "Actor":
        df = tables[metric][[f'{metric}Name',f'{metric}Gender']].merge(tables['Cast'][[f'Cast{metric}ID','CastFilmID']], left_index=True, right_on=f'Cast{metric}ID').merge(tables['Film'][['FilmBoxOfficeDollars','FilmBudgetDollars','FilmName','FilmReleaseDate','FilmLanguageID','FilmDirectorID','FilmStudioID','FilmCountryID']], left_on='CastFilmID', right_index=True)
    elif metric == "Director":
        df = tables[metric][[f'{metric}Name',f'{metric}Gender']].merge(tables['Film'][['FilmBoxOfficeDollars','FilmBudgetDollars','FilmName','FilmReleaseDate','FilmLanguageID','FilmDirectorID','FilmStudioID','FilmCountryID']], left_index=True, right_on=f'Film{metric}ID')

    if language != 'All':
        df = df[df['FilmLanguageID'] == language]

    if director != 'All':
        df = df[df['FilmDirectorID'] == director]

    if studio != 'All':
        df = df[df['FilmStudioID'] == studio]

    if country != 'All':
        df = df[df['FilmCountryID'] == country]

    df = df[df['FilmReleaseDate'].between(start_date, end_date)]

    df['Male'] = pd.get_dummies(df[f'{metric}Gender'])['Male']

    data = df[['FilmName',f'{metric}Name']].groupby('FilmName').count().merge(df[['Male','FilmName']].groupby('FilmName').sum(),left_index=True,right_index=True)[[f'{metric}Name','Male']]
    data['Percent_Male'] = data['Male']/data[f'{metric}Name']
    fig = px.histogram(data['Percent_Male'])

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#9fa6b7',title_text=f"Repartition of pourcentage of men in the main character")

    return fig
    
@app.callback(
    Output(component_id="inclusivity-plot-2", component_property="figure"),
    Input(component_id="metric-select-inclusivity", component_property="value"),
    Input(component_id="language-select-inclusivity", component_property="value"),
    Input(component_id="director-select-inclusivity", component_property="value"),
    Input(component_id="studio-select-inclusivity", component_property="value"),
    Input(component_id="country-select-inclusivity", component_property="value"),
    Input(component_id="date-select-inclusivity", component_property="start_date"),
    Input(component_id="date-select-inclusivity", component_property="end_date")
)
def update_table(metric, language, director, studio, country, start_date, end_date):
    
    if metric == "Actor":
        df = tables[metric][[f'{metric}Name',f'{metric}Gender']].merge(tables['Cast'][[f'Cast{metric}ID','CastFilmID']], left_index=True, right_on=f'Cast{metric}ID').merge(tables['Film'][['FilmBoxOfficeDollars','FilmBudgetDollars','FilmName','FilmReleaseDate','FilmLanguageID','FilmDirectorID','FilmStudioID','FilmCountryID','FilmReleaseYear']], left_on='CastFilmID', right_index=True)
    elif metric == "Director":
        df = tables[metric][[f'{metric}Name',f'{metric}Gender']].merge(tables['Film'][['FilmBoxOfficeDollars','FilmBudgetDollars','FilmName','FilmReleaseDate','FilmLanguageID','FilmDirectorID','FilmStudioID','FilmCountryID','FilmReleaseYear']], left_index=True, right_on=f'Film{metric}ID')


    if language != 'All':
        df = df[df['FilmLanguageID'] == language]

    if director != 'All':
        df = df[df['FilmDirectorID'] == director]

    if studio != 'All':
        df = df[df['FilmStudioID'] == studio]

    if country != 'All':
        df = df[df['FilmCountryID'] == country]

    df = df[df['FilmReleaseDate'].between(start_date, end_date)]

    df['Male'] = pd.get_dummies(df[f'{metric}Gender'])['Male']

    data = df[['FilmReleaseYear',f'{metric}Name']].groupby('FilmReleaseYear').count().merge(df[['Male','FilmReleaseYear']].groupby('FilmReleaseYear').sum(),left_index=True,right_index=True)[[f'{metric}Name','Male']]
    data['Percent_Male'] = data['Male']/data[f'{metric}Name']
    
    fig = go.Figure()
    fig.add_bar(x=data.index,y=data['Percent_Male'], name="% of Male")
    fig.add_bar(x=data.index,y=1-data['Percent_Male'], name="% of Female")
    fig.update_layout(barmode="relative")

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#9fa6b7',title_text=f"Repartition of pourcentage of men in the main character by year")

    return fig
    
    
@app.callback(
    Output(component_id="inclusivity-plot-3", component_property="figure"),
    Input(component_id="metric-select-inclusivity", component_property="value"),
    Input(component_id="language-select-inclusivity", component_property="value"),
    Input(component_id="director-select-inclusivity", component_property="value"),
    Input(component_id="studio-select-inclusivity", component_property="value"),
    Input(component_id="country-select-inclusivity", component_property="value"),
    Input(component_id="date-select-inclusivity", component_property="start_date"),
    Input(component_id="date-select-inclusivity", component_property="end_date")
)
def update_table(metric, language, director, studio, country, start_date, end_date):
    
    if metric == "Actor":
        df = tables[metric][[f'{metric}Name',f'{metric}Gender']].merge(tables['Cast'][[f'Cast{metric}ID','CastFilmID']], left_index=True, right_on=f'Cast{metric}ID').merge(tables['Film'][['FilmBoxOfficeDollars','FilmBudgetDollars','FilmName','FilmReleaseDate','FilmLanguageID','FilmDirectorID','FilmStudioID','FilmCountryID']], left_on='CastFilmID', right_index=True)
    elif metric == "Director":
        df = tables[metric][[f'{metric}Name',f'{metric}Gender']].merge(tables['Film'][['FilmBoxOfficeDollars','FilmBudgetDollars','FilmName','FilmReleaseDate','FilmLanguageID','FilmDirectorID','FilmStudioID','FilmCountryID']], left_index=True, right_on=f'Film{metric}ID')


    if language != 'All':
        df = df[df['FilmLanguageID'] == language]

    if director != 'All':
        df = df[df['FilmDirectorID'] == director]

    if studio != 'All':
        df = df[df['FilmStudioID'] == studio]

    if country != 'All':
        df = df[df['FilmCountryID'] == country]

    df = df[df['FilmReleaseDate'].between(start_date, end_date)]

    data= df[[f'{metric}Gender','FilmBoxOfficeDollars','FilmBudgetDollars']].groupby(f'{metric}Gender').mean()

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(x=data.index, y=data[f"FilmBoxOfficeDollars"],offsetgroup=1,name="BoxOffice Dollars" ), secondary_y=False)

    fig.add_trace(go.Bar(x=data.index, y=data[f"FilmBudgetDollars"],offsetgroup=2, name="Budget Dollars" ), secondary_y=False)

    fig.update_yaxes(tickprefix="$ ", ticksuffix="M ", secondary_y=False)

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#9fa6b7',title_text=f"Difference between Female and Male",   
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
    )


    return fig


@app.callback(
    Output(component_id="ranking-container", component_property="children"),
    Input(component_id="metric-select", component_property="value"),
    Input(component_id="language-select-ranking", component_property="value"),
    Input(component_id="director-select-ranking", component_property="value"),
    Input(component_id="studio-select-ranking", component_property="value"),
    Input(component_id="country-select-ranking", component_property="value"),
    Input(component_id="date-select-ranking", component_property="start_date"),
    Input(component_id="date-select-ranking", component_property="end_date")
)
def update_table(metric, language, director, studio, country, start_date, end_date):
    df = tables["Film"]

    if language != 'All':
        df = df[df['FilmLanguageID'] == language]

    if director != 'All':
        df = df[df['FilmDirectorID'] == director]

    if studio != 'All':
        df = df[df['FilmStudioID'] == studio]

    if country != 'All':
        df = df[df['FilmCountryID'] == country]

    df = df[df['FilmReleaseDate'].between(start_date, end_date)]

    df = df.sort_values(f"Film{metric}", ascending=False)

    if metric in ['BoxOfficeDollars', 'BudgetDollars','Benefits'] :
        format_metric = Format(precision=4, scheme=Scheme.decimal).symbol(Symbol.yes).symbol_prefix('$').symbol_suffix(' M')
    else : 
        format_metric = Format(precision=2, scheme=Scheme.decimal_integer)

    return dash_table.DataTable(
        id="procedure-stats-table",
        columns=[{'name': 'FilmName', 'id': 'FilmName'}, {'name': f"Film{metric}", 'id': f"Film{metric}",'type':'numeric','format':format_metric}],
        data=df.to_dict("records"),
        filter_action="native",
        sort_action="native",
        style_cell={
            "textOverflow": "ellipsis",
            "background-color": "#242a3b",
            "color": "#7b7d8d",
        },
        sort_mode="multi",
        page_size=10,
        style_header={"background-color": "#1f2536"},
        page_current=0
        
    )


@app.callback(
    Output(component_id="figure-ranking", component_property="figure"),
    Input(component_id="metric-select", component_property="value"),
    Input(component_id="language-select-ranking", component_property="value"),
    Input(component_id="director-select-ranking", component_property="value"),
    Input(component_id="studio-select-ranking", component_property="value"),
    Input(component_id="country-select-ranking", component_property="value"),
    Input(component_id="date-select-ranking", component_property="start_date"),
    Input(component_id="date-select-ranking", component_property="end_date"),
    Input(component_id="ranking-container", component_property="children")
)

def ranking_figure(metric, language, director, studio, country, start_date, end_date, page_count):
    df = tables["Film"]

    if language != 'All':
        df = df[df['FilmLanguageID'] == language]

    if director != 'All':
        df = df[df['FilmDirectorID'] == director]

    if studio != 'All':
        df = df[df['FilmStudioID'] == studio]

    if country != 'All':
        df = df[df['FilmCountryID'] == country]

    df = df[df['FilmReleaseDate'].between(start_date, end_date)]

    df = df[['FilmName',f"Film{metric}"]].sort_values(f"Film{metric}", ascending=False)

    page_count = page_count['props']['page_current']

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(x=df['FilmName'], y=df[f"Film{metric}"].iloc[0:10]))

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#9fa6b7')

    fig.update_yaxes(tickprefix="$ ", ticksuffix="M ", secondary_y=False)
    
    return fig
    

@app.callback(
    Output(component_id="ranking-table-title", component_property='children'),
    Input(component_id="metric-select", component_property="value")
)

def ranking_title(metric):
    return f"Ranking of film by {metric}"

@app.callback(
    Output(component_id="ages-plot-1", component_property="figure"),
    Input(component_id="metric-select-ages", component_property="value"),
    Input(component_id="language-select-ages", component_property="value"),
    Input(component_id="director-select-ages", component_property="value"),
    Input(component_id="studio-select-ages", component_property="value"),
    Input(component_id="country-select-ages", component_property="value"),
    Input(component_id="date-select-ages", component_property="start_date"),
    Input(component_id="date-select-ages", component_property="end_date")
)
def update_table(metric, language, director, studio, country, start_date, end_date):
    
    if metric == "Actor":
        df = tables[metric].merge(tables['Cast'][[f'Cast{metric}ID','CastFilmID']], left_index=True, right_on=f'Cast{metric}ID').merge(tables['Film'][['FilmBoxOfficeDollars','FilmBudgetDollars','FilmName','FilmReleaseDate','FilmLanguageID','FilmDirectorID','FilmStudioID','FilmCountryID','FilmReleaseYear']], left_on='CastFilmID', right_index=True)
    elif metric == "Director":
        df = tables[metric].merge(tables['Film'][['FilmBoxOfficeDollars','FilmBudgetDollars','FilmName','FilmReleaseDate','FilmLanguageID','FilmDirectorID','FilmStudioID','FilmCountryID','FilmReleaseYear']], left_index=True, right_on=f'Film{metric}ID')

    df['Age'] = ( df['FilmReleaseDate'] - df[f'{metric}DOB'] ) / 365
    df['Age'] = df['Age'].dt.days.round(0)
    df = df[df['Age'].notna() == True]

    if language != 'All':
        df = df[df['FilmLanguageID'] == language]

    if director != 'All':
        df = df[df['FilmDirectorID'] == director]

    if studio != 'All':
        df = df[df['FilmStudioID'] == studio]

    if country != 'All':
        df = df[df['FilmCountryID'] == country]

    df = df[df['FilmReleaseDate'].between(start_date, end_date)]

    df['-20years'] = df['Age'] < 20
    df['20-40years'] = df['Age'].between(20,39)
    df['40-60years'] = df['Age'].between(40,59)
    df['+60years'] = df['Age'] >= 60

    data= df[['-20years','20-40years','40-60years','+60years',f'{metric}Name']]
    b=1
    data['AgeCat'] = ''
    for i in ['-20years','20-40years','40-60years','+60years']:
        data.loc[data[i]==True,'AgeCat'] = i

    data = data[['AgeCat',f'{metric}Name']].groupby('AgeCat').count()

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=data.index, y=data[f"{metric}Name"],offsetgroup=1,name="Number of {metric}s by age category" ), secondary_y=False)

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#9fa6b7',title_text=f"Repartition of pourcentage of men in the main character")

    return fig
    
@app.callback(
    Output(component_id="ages-plot-2", component_property="figure"),
    Input(component_id="metric-select-ages", component_property="value"),
    Input(component_id="language-select-ages", component_property="value"),
    Input(component_id="director-select-ages", component_property="value"),
    Input(component_id="studio-select-ages", component_property="value"),
    Input(component_id="country-select-ages", component_property="value"),
    Input(component_id="date-select-ages", component_property="start_date"),
    Input(component_id="date-select-ages", component_property="end_date")
)
def update_table(metric, language, director, studio, country, start_date, end_date):
    
    if metric == "Actor":
        df = tables[metric].merge(tables['Cast'][[f'Cast{metric}ID','CastFilmID']], left_index=True, right_on=f'Cast{metric}ID').merge(tables['Film'][['FilmBoxOfficeDollars','FilmBudgetDollars','FilmName','FilmReleaseDate','FilmLanguageID','FilmDirectorID','FilmStudioID','FilmCountryID','FilmReleaseYear']], left_on='CastFilmID', right_index=True)
    elif metric == "Director":
        df = tables[metric].merge(tables['Film'][['FilmBoxOfficeDollars','FilmBudgetDollars','FilmName','FilmReleaseDate','FilmLanguageID','FilmDirectorID','FilmStudioID','FilmCountryID','FilmReleaseYear']], left_index=True, right_on=f'Film{metric}ID')

    df['Age'] = ( df['FilmReleaseDate'] - df[f'{metric}DOB'] ) / 365
    df['Age'] = df['Age'].dt.days.round(0)
    df = df[df['Age'].notna() == True]

    if language != 'All':
        df = df[df['FilmLanguageID'] == language]

    if director != 'All':
        df = df[df['FilmDirectorID'] == director]

    if studio != 'All':
        df = df[df['FilmStudioID'] == studio]

    if country != 'All':
        df = df[df['FilmCountryID'] == country]

    df = df[df['FilmReleaseDate'].between(start_date, end_date)]

    df['-20years'] = df['Age'] < 20
    df['20-40years'] = df['Age'].between(20,39)
    df['40-60years'] = df['Age'].between(40,59)
    df['+60years'] = df['Age'] >= 60

    data = df[['FilmReleaseYear',f'{metric}Name']].groupby('FilmReleaseYear').count().merge(df[['-20years','20-40years','40-60years','+60years','FilmReleaseYear']].groupby('FilmReleaseYear').sum(),left_index=True,right_index=True)[[f'{metric}Name','-20years','20-40years','40-60years','+60years']]
    
    for i in ['-20years','20-40years','40-60years','+60years']:
        data[i] = data[i]/data[f'{metric}Name']


    fig = go.Figure()
    fig.add_bar(x=data.index,y=data['-20years'], name="% of -20 years old")
    fig.add_bar(x=data.index,y=data['20-40years'], name="% of 20-40 years old")
    fig.add_bar(x=data.index,y=data['40-60years'], name="% of 40-60 years old")
    fig.add_bar(x=data.index,y=data['+60years'], name="% of +60 years old")   
    fig.update_layout(barmode="relative")

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#9fa6b7',title_text=f"Repartition of the age category in the main character by year")

    return fig
    
    
@app.callback(
    Output(component_id="ages-plot-3", component_property="figure"),
    Input(component_id="metric-select-ages", component_property="value"),
    Input(component_id="language-select-ages", component_property="value"),
    Input(component_id="director-select-ages", component_property="value"),
    Input(component_id="studio-select-ages", component_property="value"),
    Input(component_id="country-select-ages", component_property="value"),
    Input(component_id="date-select-ages", component_property="start_date"),
    Input(component_id="date-select-ages", component_property="end_date")
)
def update_table(metric, language, director, studio, country, start_date, end_date):
    
    if metric == "Actor":
        df = tables[metric].merge(tables['Cast'][[f'Cast{metric}ID','CastFilmID']], left_index=True, right_on=f'Cast{metric}ID').merge(tables['Film'][['FilmBoxOfficeDollars','FilmBudgetDollars','FilmName','FilmReleaseDate','FilmLanguageID','FilmDirectorID','FilmStudioID','FilmCountryID','FilmReleaseYear']], left_on='CastFilmID', right_index=True)
    elif metric == "Director":
        df = tables[metric].merge(tables['Film'][['FilmBoxOfficeDollars','FilmBudgetDollars','FilmName','FilmReleaseDate','FilmLanguageID','FilmDirectorID','FilmStudioID','FilmCountryID','FilmReleaseYear']], left_index=True, right_on=f'Film{metric}ID')

    df['Age'] = ( df['FilmReleaseDate'] - df[f'{metric}DOB'] ) / 365
    df['Age'] = df['Age'].dt.days.round(0)
    df = df[df['Age'].notna() == True]
    
    if language != 'All':
        df = df[df['FilmLanguageID'] == language]

    if director != 'All':
        df = df[df['FilmDirectorID'] == director]

    if studio != 'All':
        df = df[df['FilmStudioID'] == studio]

    if country != 'All':
        df = df[df['FilmCountryID'] == country]

    df = df[df['FilmReleaseDate'].between(start_date, end_date)]

    df['-20years'] = df['Age'] < 20
    df['20-40years'] = df['Age'].between(20,39)
    df['40-60years'] = df['Age'].between(40,59)
    df['+60years'] = df['Age'] >= 60

    data= df[['-20years','20-40years','40-60years','+60years','FilmBoxOfficeDollars','FilmBudgetDollars']]

    b = 1
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    data['AgeCat'] = ''
    for i in ['-20years','20-40years','40-60years','+60years']:
        data.loc[data[i]==True,'AgeCat'] = i

    data= data[['AgeCat','FilmBoxOfficeDollars','FilmBudgetDollars']].groupby('AgeCat').mean()

    
    fig.add_trace(go.Bar(x=data.index, y=data[f"FilmBoxOfficeDollars"],offsetgroup=1,name="BoxOffice Dollars" ), secondary_y=False)

    fig.add_trace(go.Bar(x=data.index, y=data[f"FilmBudgetDollars"],offsetgroup=2, name="Budget Dollars" ), secondary_y=False)

    fig.update_yaxes(tickprefix="$ ", ticksuffix="M ", secondary_y=False)

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#9fa6b7',title_text=f"Difference between age category",   
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
    )


    return fig


@app.callback(
    Output(component_id="geo-plot", component_property="figure"),
    Input(component_id="metric-select-geo", component_property="value"),
    Input(component_id="language-select-geo", component_property="value"),
    Input(component_id="director-select-geo", component_property="value"),
    Input(component_id="studio-select-geo", component_property="value"),
    Input(component_id="country-select-geo", component_property="value"),
    Input(component_id="date-select-geo", component_property="start_date"),
    Input(component_id="date-select-geo", component_property="end_date")
)
def update_table(metric, language, director, studio, country, start_date, end_date):
    
    df = tables['Film'].merge(tables["Country"], left_on='FilmCountryID', right_index=True)

    if language != 'All':
        df = df[df['FilmLanguageID'] == language]

    if director != 'All':
        df = df[df['FilmDirectorID'] == director]

    if studio != 'All':
        df = df[df['FilmStudioID'] == studio]

    if country != 'All':
        df = df[df['FilmCountryID'] == country]

    df = df[df['FilmReleaseDate'].between(start_date, end_date)]

    if metric == "Average":
        data = df[['FilmBoxOfficeDollars', 'FilmBudgetDollars', 'FilmBenefits','FilmReleaseYear']].groupby('FilmReleaseYear').mean()
    if metric == "Total":
        data = df[['FilmBoxOfficeDollars', 'FilmBudgetDollars', 'FilmBenefits','FilmReleaseYear']].groupby('FilmReleaseYear').sum()
    
    df = df[['CountryCode','FilmBoxOfficeDollars','FilmBudgetDollars','FilmBenefits']].groupby('CountryCode').mean().merge(df[['CountryCode','FilmName']].groupby('CountryCode').count(),left_index=True,right_index=True)

    

    fig = go.Figure(data=go.Choropleth(
    locations = df.index,
    z = df[f'Film{metric}'],
    text = df.index,
    autocolorscale=True,
    colorscale="rdylbu",
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_ticksuffix = ' M',
    colorbar_tickprefix = '$ ',
    colorbar_title = metric,
    ))

    fig2 = px.scatter_geo(df, locations=df.index,
                        size="FilmName")

    fig.add_trace(fig2.data[0])

    fig.update_layout(
            autosize=False,
            margin = dict(
                    l=0,
                    r=0,
                    b=0,
                    t=0,
                    pad=4,
                    autoexpand=True
                ),
            #     height=400,
        )
    
    fig.update_geos(
    visible=False, resolution=50,
    showcountries=True, countrycolor="RebeccaPurple", bgcolor='rgba(0,0,0,0)'
)
    fig.update_traces(hovertemplate = 'BoxOffice=$ %{text}M<br>iso_alpha=%{location}<extra></extra>', text = df[f'Film{metric}'])
    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)')  ) 
  


    return fig




if __name__ == '__main__':
	app.run(debug=True)

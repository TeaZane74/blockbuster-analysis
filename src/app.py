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
            dcc.Tab(label='Evolution of Cinema Industry', children=[evo.layout()], style=tab_style,selected_style=tab_selected_style),
            dcc.Tab(label='Actors success', children=[actors.layout()], style=tab_style,selected_style=tab_selected_style),
            dcc.Tab(label='Directors success', children=[dr.layout()], style=tab_style,selected_style=tab_selected_style),
            dcc.Tab(label='Studios success', children=[st.layout()], style=tab_style,selected_style=tab_selected_style),
            dcc.Tab(label='Gender Analysis in Cinema', children=[inclusivity.layout()], style=tab_style,selected_style=tab_selected_style),
            dcc.Tab(label='Age Analysis in Cinema', children=[], style=tab_style,selected_style=tab_selected_style)
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

@callback(
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

    df['Male'] = pd.get_dummies(df['ActorGender'])['Male']

    data = df.groupby('FilmName').count().merge(df.groupby('FilmName').sum(),left_index=True,right_index=True)[['ActorName','Male_y']]
    data['%Male'] = data['Male_y']/data['ActorName']
    fig = px.histogram(data['%Male'])

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#9fa6b7',title_text=f"Repartition of pourcentage of men in the main role")

    return fig
    
@callback(
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

    df['Male'] = pd.get_dummies(df['ActorGender'])['Male']

    data = df.groupby('FilmReleaseYear').count().merge(df.groupby('FilmReleaseYear').sum(),left_index=True,right_index=True)[['ActorName','Male_y']]
    data['%Male'] = data['Male_y']/data['ActorName']
    
    fig = go.Figure()
    fig.add_bar(x=data.index,y=data['%Male'], name="% of Male")
    fig.add_bar(x=data.index,y=1-data['%Male'], name="% of Female")
    fig.update_layout(barmode="relative")

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#9fa6b7',title_text=f"Repartition of pourcentage of men in the main role by year")

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

    data= df.groupby('ActorGender').mean()

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


@callback(
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


@callback(
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
    

@callback(
    Output(component_id="ranking-table-title", component_property='children'),
    Input(component_id="metric-select", component_property="value")
)

def ranking_title(metric):
    return f"Ranking of film by {metric}"







if __name__ == '__main__':
	app.run(debug=True)

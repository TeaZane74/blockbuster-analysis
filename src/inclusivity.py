from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Symbol, Scheme
import plotly.graph_objects as go
import plotly.express  as px
from plotly.subplots import make_subplots
import pandas as pd



from utils import generate_dropdown_option
from app import app
from data import tables


def inclusivity_tab(tables, metric):
    return html.Div(className="container scalable", children=[
        html.Div(
            id="upper-container-inclusivity",
            className="row",
            children=[
                html.Div(
                    id="upper-left-inclusivity",
                    className="six columns",
                    children=[
                        html.Br(),
                        html.P(
                            className="section-title",
                            children="Rank by :",
                        ),
                        html.Div(
                            id="metric-select-outer-inclusivity",
                            className="control-row-2",
                            children=[
                                html.Label("Select a Metric"),
                                dcc.Dropdown(
                                    id="metric-select-inclusivity",
                                    options=[{"label": i, "value": i} for i in metric],
                                    value=metric[0],
                                ),
                            ],
                        ),
                        html.Br(),
                        html.P(className='section-title', children="Filters"),
                        html.Div(
                            className="control-row-1",
                            id="filter-select-outer-inclusivity",
                            children=[
                                html.Div(
                                    children=[
                                        html.Label("Filter by language"),
                                        dcc.Dropdown(
                                            id="language-select-inclusivity",
                                            options=generate_dropdown_option(tables['Language'].to_dict('dict')['Language'], all=True),
                                            value="All"
                                        )
                                    ]
                                ),
                                html.Div(
                                    children=[
                                        html.Label("Filter by Country"),
                                        dcc.Dropdown(
                                            id="country-select-inclusivity",
                                            options=generate_dropdown_option(tables['Country'].to_dict('dict')['CountryName'], all=True),
                                            value="All"
                                        )
                                    ]
                                ),
                                html.Div(
                                    children=[
                                        html.Label("Filter by Director"),
                                        dcc.Dropdown(
                                            id="director-select-inclusivity",
                                            options=generate_dropdown_option(tables['Director'].to_dict('dict')['DirectorName'], all=True),
                                            value="All"
                                        )
                                    ]
                                ),
                                html.Div(
                                    children=[
                                        html.Label("Filter by Studio"),
                                        dcc.Dropdown(
                                            id="studio-select-inclusivity",
                                            options=generate_dropdown_option(tables['Studio'].to_dict('dict')['StudioName'], all=True),
                                            value="All",
                                            searchable=True,
                                            clearable=True
                                        )
                                    ]
                                )
                            ]
                        ),
                        html.Br(),
                        html.Div(
                            className='control-row-2',
                            children=[
                                html.Div(
                                    children=[
                                        html.Label("Filter by date"),
                                        dcc.DatePickerRange(
                                            id="date-select-inclusivity",
                                            start_date=tables['Film']['FilmReleaseDate'].min(),
                                            end_date=tables['Film']['FilmReleaseDate'].max()
                                        )
                                    ]
                                )
                            ]
                        ),
                    html.Div(children=[
                    html.Br(),
                    dcc.Graph(id="inclusivity-plot-3")
                    ]),

                    ],
                ),
                html.Div(
                    className="six columns",
                    id="inclusivity-table",
                    children=[
                        html.Div(
                            id="table-inclusivity",
                            children=[
                                dcc.Graph(id="inclusivity-plot-1"),
                                dcc.Graph(id="inclusivity-plot-2")
                            ],
                        ),
                    ],
                ),
            ]
        ),
    ])

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

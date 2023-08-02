from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Symbol, Scheme
import plotly.graph_objects as go
from plotly.subplots import make_subplots


from utils import generate_dropdown_option
from app import app
from data import tables


def director_tab(tables, metric):
    return html.Div(className="container scalable", children=[
        html.Div(
            id="upper-container-director",
            className="row",
            children=[
                html.Div(
                    id="upper-left-director",
                    className="six columns",
                    children=[
                        html.Br(),
                        html.P(
                            className="section-title",
                            children="Rank by :",
                        ),
                        html.Div(
                            id="metric-select-outer-director",
                            className="control-row-2",
                            children=[
                                html.Div(children=[
                                    html.Label("Select a Metric"),
                                    dcc.Dropdown(
                                        id="metric-select-director",
                                        options=[{"label": i, "value": i} for i in metric],
                                        value=metric[0],
                                    )]),

                                    html.Div(children=[
                                    html.Label("Select a Metric"),
                                    dcc.Dropdown(
                                        id="metric-select-director-2",
                                        options=[{"label": i, "value": i} for i in ['Average','Total']],
                                        value='Average',
                                    )]),
                            ],
                        ),
                        html.Br(),
                        html.P(className='section-title', children="Filters"),
                        html.Div(
                            className="control-row-1",
                            id="filter-select-outer-director",
                            children=[
                                html.Div(
                                    children=[
                                        html.Label("Filter by language"),
                                        dcc.Dropdown(
                                            id="language-select-director",
                                            options=generate_dropdown_option(tables['Language'].to_dict('dict')['Language'], all=True),
                                            value="All"
                                        )
                                    ]
                                ),
                                html.Div(
                                    children=[
                                        html.Label("Filter by Country"),
                                        dcc.Dropdown(
                                            id="country-select-director",
                                            options=generate_dropdown_option(tables['Country'].to_dict('dict')['CountryName'], all=True),
                                            value="All"
                                        )
                                    ]
                                ),
                                html.Div(
                                    children=[
                                        html.Label("Filter by Director"),
                                        dcc.Dropdown(
                                            id="director-select-director",
                                            options=generate_dropdown_option(tables['Director'].to_dict('dict')['DirectorName'], all=True),
                                            value="All"
                                        )
                                    ]
                                ),
                                html.Div(
                                    children=[
                                        html.Label("Filter by Studio"),
                                        dcc.Dropdown(
                                            id="studio-select-director",
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
                                            id="date-select-director",
                                            start_date=tables['Film']['FilmReleaseDate'].min(),
                                            end_date=tables['Film']['FilmReleaseDate'].max()
                                        )
                                    ]
                                )
                            ]
                        ),
                    ],
                ),
                html.Div(
                    className="six columns",
                    id="director-table",
                    children=[
                        html.Div(
                            id="table-director",
                            children=[
                                dcc.Graph(id="director-plot"),
                            ],
                        ),
                    ],
                ),
            ]
        ),

        html.Div(children=[dcc.Graph(id="figure-director")])
    ])

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





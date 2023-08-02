from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Symbol, Scheme
import plotly.graph_objects as go
from plotly.subplots import make_subplots


from utils import generate_dropdown_option
from app import app
from data import tables


def studio_tab(tables, metric):
    return html.Div(className="container scalable", children=[
        html.Div(
            id="upper-container-studio",
            className="row",
            children=[
                html.Div(
                    id="upper-left-studio",
                    className="six columns",
                    children=[
                        html.Br(),
                        html.P(
                            className="section-title",
                            children="Rank by :",
                        ),
                        html.Div(
                            id="metric-select-outer-studio",
                            className="control-row-2",
                            children=[
                                html.Div(children=[
                                    html.Label("Select a Metric"),
                                    dcc.Dropdown(
                                        id="metric-select-studio",
                                        options=[{"label": i, "value": i} for i in metric],
                                        value=metric[0],
                                    )]),

                                    html.Div(children=[
                                    html.Label("Select a Metric"),
                                    dcc.Dropdown(
                                        id="metric-select-studio-2",
                                        options=[{"label": i, "value": i} for i in ['Average','Total']],
                                        value='Average',
                                    )]),
                            ],
                        ),
                        html.Br(),
                        html.P(className='section-title', children="Filters"),
                        html.Div(
                            className="control-row-1",
                            id="filter-select-outer-studio",
                            children=[
                                html.Div(
                                    children=[
                                        html.Label("Filter by language"),
                                        dcc.Dropdown(
                                            id="language-select-studio",
                                            options=generate_dropdown_option(tables['Language'].to_dict('dict')['Language'], all=True),
                                            value="All"
                                        )
                                    ]
                                ),
                                html.Div(
                                    children=[
                                        html.Label("Filter by Country"),
                                        dcc.Dropdown(
                                            id="country-select-studio",
                                            options=generate_dropdown_option(tables['Country'].to_dict('dict')['CountryName'], all=True),
                                            value="All"
                                        )
                                    ]
                                ),
                                html.Div(
                                    children=[
                                        html.Label("Filter by Director"),
                                        dcc.Dropdown(
                                            id="director-select-studio",
                                            options=generate_dropdown_option(tables['Director'].to_dict('dict')['DirectorName'], all=True),
                                            value="All"
                                        )
                                    ]
                                ),
                                html.Div(
                                    children=[
                                        html.Label("Filter by Studio"),
                                        dcc.Dropdown(
                                            id="studio-select-studio",
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
                                            id="date-select-studio",
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
                    id="studio-table",
                    children=[
                        html.Div(
                            id="table-studio",
                            children=[
                                dcc.Graph(id="studio-plot"),
                            ],
                        ),
                    ],
                ),
            ]
        ),

        html.Div(children=[dcc.Graph(id="figure-studio")])
    ])

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





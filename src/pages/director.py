import dash
from dash import Dash, dcc, html, dash_table,callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Symbol, Scheme
import plotly.graph_objects as go
from plotly.subplots import make_subplots


from utils import generate_dropdown_option
from data import tables

#dash.register_page(__name__)

def layout():
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
                                        options=[{"label": i, "value": i} for i in ['BoxOfficeDollars', 'BudgetDollars', 'Benefits']],
                                        value=['BoxOfficeDollars', 'BudgetDollars', 'Benefits'][0],
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
    ])



import dash
from dash import Dash, dcc, html, dash_table,callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Symbol, Scheme
import plotly.graph_objects as go
import plotly.express  as px
from plotly.subplots import make_subplots
import pandas as pd

#dash.register_page(__name__)

from utils import generate_dropdown_option
from data import tables


def layout():
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
                                    options=[{"label": i, "value": i} for i in ['Actor','Director']],
                                    value='Actor',
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



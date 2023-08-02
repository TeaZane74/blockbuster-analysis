from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Symbol, Scheme
import plotly.graph_objects as go
from plotly.subplots import make_subplots


from utils import generate_dropdown_option
from app import app
from data import tables


def evolution_tab(tables, metric):
    return html.Div(className="container scalable", children=[
        html.Div(
            id="upper-container-evolution",
            className="row",
            children=[
                html.Div(
                    id="upper-left-evolution",
                    className="six columns",
                    children=[
                        html.Br(),
                        html.P(
                            className="section-title",
                            children="Rank by :",
                        ),
                        html.Div(
                            id="metric-select-outer-evolution",
                            className="control-row-2",
                            children=[
                                html.Label("Select a Metric"),
                                dcc.Dropdown(
                                    id="metric-select-evolution",
                                    options=[{"label": i, "value": i} for i in metric],
                                    value=metric[0],
                                ),
                            ],
                        ),
                        html.Br(),
                        html.P(className='section-title', children="Filters"),
                        html.Div(
                            className="control-row-1",
                            id="filter-select-outer-evolution",
                            children=[
                                html.Div(
                                    children=[
                                        html.Label("Filter by language"),
                                        dcc.Dropdown(
                                            id="language-select-evolution",
                                            options=generate_dropdown_option(tables['Language'].to_dict('dict')['Language'], all=True),
                                            value="All"
                                        )
                                    ]
                                ),
                                html.Div(
                                    children=[
                                        html.Label("Filter by Country"),
                                        dcc.Dropdown(
                                            id="country-select-evolution",
                                            options=generate_dropdown_option(tables['Country'].to_dict('dict')['CountryName'], all=True),
                                            value="All"
                                        )
                                    ]
                                ),
                                html.Div(
                                    children=[
                                        html.Label("Filter by Director"),
                                        dcc.Dropdown(
                                            id="director-select-evolution",
                                            options=generate_dropdown_option(tables['Director'].to_dict('dict')['DirectorName'], all=True),
                                            value="All"
                                        )
                                    ]
                                ),
                                html.Div(
                                    children=[
                                        html.Label("Filter by Studio"),
                                        dcc.Dropdown(
                                            id="studio-select-evolution",
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
                                            id="date-select-evolution",
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
                    id="evolution-table",
                    children=[
                        html.Div(
                            id="table-evolution",
                            children=[
                                dcc.Graph(id="evolution-plot"),
                            ],
                        ),
                    ],
                ),
            ]
        ),

        html.Div(children=[dcc.Graph(id="figure-evolution")])
    ])

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





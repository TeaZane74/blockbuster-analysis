from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Symbol, Scheme
import plotly.graph_objects as go
from plotly.subplots import make_subplots


from utils import generate_dropdown_option
import app
from app import app
from data import tables

def ranking_tab(tables, metric):
    return html.Div(className="container scalable", children=[
        html.Div(
            id="upper-container",
            className="row",
            children=[
                html.Div(
                    id="upper-left",
                    className="six columns",
                    children=[
                        html.Br(),
                        html.P(
                            className="section-title",
                            children="Rank by :",
                        ),
                        html.Div(
                            id="metric-select-outer",
                            className="control-row-2",
                            children=[
                                html.Label("Select a Metric"),
                                dcc.Dropdown(
                                    id="metric-select",
                                    options=[{"label": i, "value": i} for i in metric],
                                    value=metric[0],
                                ),
                            ],
                        ),
                        html.Br(),
                        html.P(className='section-title', children="Filters"),
                        html.Div(
                            className="control-row-1",
                            id="filter-select-outer",
                            children=[
                                html.Div(
                                    children=[
                                        html.Label("Filter by language"),
                                        dcc.Dropdown(
                                            id="language-select-ranking",
                                            options=generate_dropdown_option(tables['Language'].to_dict('dict')['Language'], all=True),
                                            value="All"
                                        )
                                    ]
                                ),
                                html.Div(
                                    children=[
                                        html.Label("Filter by Country"),
                                        dcc.Dropdown(
                                            id="country-select-ranking",
                                            options=generate_dropdown_option(tables['Country'].to_dict('dict')['CountryName'], all=True),
                                            value="All"
                                        )
                                    ]
                                ),
                                html.Div(
                                    children=[
                                        html.Label("Filter by Director"),
                                        dcc.Dropdown(
                                            id="director-select-ranking",
                                            options=generate_dropdown_option(tables['Director'].to_dict('dict')['DirectorName'], all=True),
                                            value="All"
                                        )
                                    ]
                                ),
                                html.Div(
                                    children=[
                                        html.Label("Filter by Studio"),
                                        dcc.Dropdown(
                                            id="studio-select-ranking",
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
                                            id="date-select-ranking",
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
                    id="ranking-table",
                    children=[
                        html.Div(
                            id="table-ranking",
                            children=[
                                html.P(id="ranking-table-title"),
                                html.Div(id="ranking-container"),
                            ],
                        ),
                    ],
                ),
            ]
        ),

        html.Div(children=[dcc.Graph(id="figure-ranking")])
    ])

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
import dash
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd


from data import tables





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

layout = html.Div(
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
            dcc.Tab(label='Ranking By Film',children=[rk.ranking_tab(tables,['BoxOfficeDollars', 'BudgetDollars', 'OscarNominations', 'OscarWins', 'Benefits'])], style=tab_style,selected_style=tab_selected_style),
            dcc.Tab(label='Evolution of Cinema Industry', children=[evo.evolution_tab(tables,['Average','Total'])], style=tab_style,selected_style=tab_selected_style),
            dcc.Tab(label='Actors success', children=[actors.actor_tab(tables,['BoxOfficeDollars', 'BudgetDollars', 'Benefits'])], style=tab_style,selected_style=tab_selected_style),
            dcc.Tab(label='Directors success', children=[dr.director_tab(tables,['BoxOfficeDollars', 'BudgetDollars', 'Benefits'])], style=tab_style,selected_style=tab_selected_style),
            dcc.Tab(label='Studios success', children=[st.studio_tab(tables,['BoxOfficeDollars', 'BudgetDollars', 'Benefits'])], style=tab_style,selected_style=tab_selected_style),
            dcc.Tab(label='Gender Analysis in Cinema', children=[inclusivity.inclusivity_tab(tables,['BoxOfficeDollars', 'BudgetDollars', 'Benefits'])], style=tab_style,selected_style=tab_selected_style),
            dcc.Tab(label='Age Analysis in Cinema', children=[inclusivity.inclusivity_tab(tables,['BoxOfficeDollars', 'BudgetDollars', 'Benefits'])], style=tab_style,selected_style=tab_selected_style)
        ], style=tabs_styles)
    ],
)

from dash import Dash, html, dcc
from data import tables
import dash
import pages.actors as ac




app = Dash(__name__, use_pages=False, suppress_callback_exceptions=True)
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
            dcc.Tab(label='Ranking By Film',children=[ac.layout()], style=tab_style,selected_style=tab_selected_style),

        ], style=tabs_styles),
	    
    ],
)


if __name__ == '__main__':
	app.run(debug=True)

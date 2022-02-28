import os
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State

from stylesheets import style as st

from pages import home
from pages import about
from usecase import parkinson as PKS_DS
from main_app import app

pages = ['home',
'about',
'parkinson',
]

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/home"]:
        return home.page_render_code
    elif pathname == "/about":
        return about.page_render_code
    elif pathname == "/parkinson":
        return PKS_DS.page_render_code
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

@app.callback([Output(f"{i}-link", "active") for i in pages], [Input("url", "pathname")])
def toggle_active_links(pathname):
    if pathname == "/":
        return True, False, False
    return [pathname == f"/{i}" for i in pages]

@app.server.route('/static/<path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)


sidebar = html.Div(
    [
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/home", id="home-link", className = "NavLinks"),
                dbc.NavLink("About", href="/about", id="about-link", className = "NavLinks"),

                html.Div([
                    html.H2("Project Demo", id = "demo-header"),
                    html.Hr(style = {'margin-bottom' : '1vw','margin-top' : '0', 'border' : '0', 'clear' : 'both', 'display' : 'block', 'width' : '96%', 'background-color' : '#FFAE00', 'height' : '1px'}),
                    dbc.NavLink("Parkinson's Disease", href="/parkinson", id="parkinson-link", className = "NavLinks"),
                ])
            ], vertical=True, pills=True)], className = "leftScrollContent", style = st.SIDEBAR_STYLE)

content = html.Div(id="page-content", style= st.CONTENT_STYLE)
makeLayout = html.Div([dcc.Location(id="url"), sidebar, content])

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import base64
import os
import json
import numpy as np
from dash.dependencies import Input, Output

from stylesheets import style as st
from main_app import app

def randomise():
    a = np.arange(1,9)
    np.random.shuffle(a)
    return a[:4]

f = open('usecase/pks.json',)
data = json.load(f)
pks_classes = data['classes']
f.close()

def explore_render_code():
    return html.Div([
                html.Div([
                    html.Div([
                        html.H3("                    Image Samples", style = {'white-space' : 'pre','margin-top' : '1.5vw', 'text-align' : 'center', 'font-size' : '1.7vw'}),
                        html.Div(children = dbc.Button('Randomize', color="primary", id='pks_refresh', style=st.PKS_RELOAD_BUTTON_STYLE), style=st.PKS_RELOAD_STYLE),
                    ], style = st.PKS_EXPLORE_HEADER_STYLE),
                    html.Hr(style = {'margin-bottom' : '1vw'}),
                    html.Div(id = 'pks_explore_output'),
            ])
        ])

@app.callback(Output('pks_explore_output', 'children'), [Input('pks_refresh', 'n_clicks')])
def refresh_explore(clicks):
    randomiser = randomise()
    return html.Div([
        ### Grid for images
        html.Div([
            html.H1(pks_classes[0], style = st.PKS_TEXT_IN_GRID),
            html.Img(src = app.get_asset_url(f'images/positive/{randomiser[0]}.png'), style = st.PKS_IMAGE_IN_GRID),
            html.Img(src = app.get_asset_url(f'images/positive/{randomiser[1]}.png'), style = st.PKS_IMAGE_IN_GRID),
            html.Img(src = app.get_asset_url(f'images/positive/{randomiser[2]}.png'), style = st.PKS_IMAGE_IN_GRID),
            html.Img(src = app.get_asset_url(f'images/positive/{randomiser[3]}.png'), style = st.PKS_IMAGE_IN_GRID),
        ], style = st.PKS_IMAGE_GRID_STYLE),

        html.Div([
            html.H1(pks_classes[1], style = st.PKS_TEXT_IN_GRID),
            html.Img(src = app.get_asset_url(f'images/negative/{randomiser[0]}.png'), style = st.PKS_IMAGE_IN_GRID),
            html.Img(src = app.get_asset_url(f'images/negative/{randomiser[1]}.png'), style = st.PKS_IMAGE_IN_GRID),
            html.Img(src = app.get_asset_url(f'images/negative/{randomiser[2]}.png'), style = st.PKS_IMAGE_IN_GRID),
            html.Img(src = app.get_asset_url(f'images/negative/{randomiser[3]}.png'), style = st.PKS_IMAGE_IN_GRID),
        ], style = st.PKS_IMAGE_GRID_STYLE),
    ], style = st.PKS_EXPLORE_STYLE)

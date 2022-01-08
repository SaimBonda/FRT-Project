import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from stylesheets import style as st
from main_app import app

page_render_code = html.Div([
html.Div([
        html.H1("PROJECT SUBMISSION", style = {'text-align' : 'center', 'font-size' : '4vw', 'color' : '#FFAE00'}),
        html.H3("Predicting the onset of Parkinson's disease", style = {'text-align' : 'center', 'font-size' : '2vw'}),
        html.H3("Saim Bonda (iambondasaim@gmail.com)", style = {'text-align' : 'center', 'font-size' : '2vw'}),
    ], style = st.HOME_DIV),
])
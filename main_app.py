import dash
import dash_bootstrap_components as dbc

ext_css = [dbc.themes.BOOTSTRAP, {
    'href': 'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
    'rel': 'stylesheet',
    'integrity': 'sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf',
    'crossorigin': 'anonymous'
}]
ext_js = []
app = dash.Dash(__name__,title='FRT Project',external_stylesheets=ext_css, external_scripts = ext_js)

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

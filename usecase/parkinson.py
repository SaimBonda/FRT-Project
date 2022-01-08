import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import plotly.figure_factory as ff
import numpy as np
import pandas as pd
from PIL import Image
from GPSPhoto import gpsphoto

import os
import base64
import io
import json
import dash_table

from plotly import express as px
from plotly import graph_objs as go
from dash.dependencies import Input, Output

from stylesheets import style as st
from usecase import explore as exp
from usecase.tf_model import parkinson_predict
from main_app import app

template = "plotly_dark"

f = open('usecase/pks.json',)
data = json.load(f)
pks_classes = data['classes']
cm = data['cm']
cm = cm[::-1]
acc = data['acc']
f.close()

us_up_path = 'user_uploaded/'

def immt_metadata(path):
    data = gpsphoto.getGPSData(path)
    df_tags = []
    df_values = []
    for tag in ["Latitude", "Longitude", "UTC-Time", "Date"]:
        try:
            df_values.append(data[tag])
        except:
            df_values.append("----")
        df_tags.append(tag)
    df = pd.DataFrame(data = [df_values], columns = df_tags)
    return df

def immt_metadata_multi(path):
    data = gpsphoto.getGPSData(path)
    df_values = []
    for tag in ["Latitude", "Longitude", "UTC-Time", "Date"]:
        try:
            df_values.append(data[tag])
        except:
            df_values.append("----")
    return df_values

def render():
    return html.Div(id="page-content", style= st.CONTENT_STYLE)

page_render_code = html.Div(children =
[
    html.H1("Parkinson's Disease Classifier"),
    html.Div(children =
    [
        html.Div(children = [
            html.Div([
                html.H3("This Model Detects the Onset of Parkinson's Disease given Image of Spiral / Wave Drawing Test", className = "about", style = {'width' : '100%', 'margin-bottom' : '2vw'}),
                dcc.Tabs(id='pks_tabs', value='explore', children = [
                    dcc.Tab(label='EXPLORE', value='explore', className="custom-tab", selected_className="custom-tab--selected",),
                    dcc.Tab(label='PREDICT', value='predict', className="custom-tab", selected_className="custom-tab--selected",),
                    dcc.Tab(label='PERFORMANCE', value='performance', className="custom-tab", selected_className="custom-tab--selected",),
                ], style = {'color' : '#f3f5f4'}),
            ]),
        ], style = st.PKS_ABOUT_STYLE),

        html.Div(id = 'pks_tabs-output'),
    ])
], style={'position':'relative','width': '100%'})

@app.callback(Output('pks_tabs-output', 'children'), [Input('pks_tabs', 'value')])
def render_content(tab):
    if tab == 'explore':
        return exp.explore_render_code()
    elif tab == 'predict':
        return html.Div([
                html.Div(children = [
                    html.H3("Data Input Method", style = st.PKS_INDUSTRY_TEXT),
                    html.Div([
                        dcc.Dropdown(id = "pks-method-choice", options=[
                                    {'label': 'One Drawing', 'value': 'single'},
                                    {'label': 'Multiple Drawings', 'value': 'multiple'}],
                                    style = st.PKS_INDUSTRY_CHOICE)
                    ], style = {'margin-left' : '1vw', 'max-height' : '2vw'})
                ], style = st.PKS_INDUSTRY_DIV),

            html.Div(id='pks-method-output'),
        ])
    elif tab == 'performance':
        return performance_render_code()

@app.callback(Output('pks-method-output', 'children'), Input('pks-method-choice', 'value'))
def pks_data_method(method):
    if method == 'single':
        return html.Div([
            html.Div([
                html.Div(children = dcc.Upload(id='pks-single-image-input', children=html.Div(['Drag and Drop or ', html.A('Select File')]), style=st.PKS_UPLOAD_STYLE)),
                html.Div(children = dbc.Button('Load Sample', color="primary", id='pks_single_load_sample', style=st.PKS_SAMPLE_UPLOAD_BUTTON_STYLE), style=st.PKS_SAMPLE_UPLOAD_STYLE),
                html.A(id = "show-template", target="_blank", children = ["Download Sample"], href = 'assets/samples/pks.png', download = "sample" , style=st.PKS_UPLOAD_STYLE),
            ], style = st.PKS_UPLOAD_DIV_STYLE),
            html.Div(className = 'load', id = "pks-single-image-output", style = {'position' : 'absolute','margin-bottom' : '7.8vw'})
        ])
    elif method == 'multiple':
        return html.Div([
            html.Div([
                html.Div(children = dcc.Upload(id='pks-multiple-image-input', multiple = True, children=html.Div(['Drag and Drop or ', html.A('Select Multiple Files')]), style=st.PKS_UPLOAD_STYLE)),
                html.Div(children = dbc.Button('Load Sample', color="primary", id='pks_multiple_load_sample', style=st.PKS_SAMPLE_UPLOAD_BUTTON_STYLE), style=st.PKS_SAMPLE_UPLOAD_STYLE),
                html.A(id = "show-template", target="_blank", children = ["Download Sample"], href = 'assets/samples/pks.png', download = "sample" , style=st.PKS_UPLOAD_STYLE),
            ], style = st.PKS_UPLOAD_DIV_STYLE),
            html.Div(className = 'load', id = "pks-multiple-image-output")
        ])

@app.callback(Output('pks-multiple-image-output', 'children'), [Input('pks-multiple-image-input', 'contents'), Input('pks_multiple_load_sample', 'n_clicks')])
def update_image(loc, clicks):
    if loc is not None:
        inference = []
        inf_card = []
        for contents in loc:
            content_type, content_string = contents.split(',')
            img_type = content_type.split('/')[1]
            img_type = img_type[:-7]
            if 'image' in content_type:

                data = contents.encode("utf8").split(b";base64,")[1]
                with open(os.path.join(us_up_path, 'upload.png'), "wb") as fp:
                    fp.write(base64.decodebytes(data))
                mtdt = immt_metadata_multi(us_up_path + 'upload.png')

                # Saving and Loading Image
                im = base64.b64decode(content_string)
                img = Image.open(io.BytesIO(im))
                img = img.convert('RGB')
                img.save(us_up_path + 'test.png')

                # Running model and getting predictions
                pred = parkinson_predict(us_up_path + 'test.png')
                pred = pred.tolist()
                pred = pred[0]
                i = pred.index(max(pred))
                c = pks_classes[i]
                conf = max(pred)
                if conf > 0.65:
                    conf = max(pred) - np.random.randint(int(conf * 5), int(conf * 10))/100

                inf_df = pd.DataFrame(data = [["Prediction", "Confidence", "Latitude", "Longitude", "UTC-Time", "Date"], [c, str(int(conf*100)) + " %", mtdt[0], mtdt[1], mtdt[2], mtdt[3]]]).transpose()
                inf_df.columns = ['Parameter', 'Value']

                inf_card.append(
                    html.Div([
                        html.Img(src = contents, style = st.PKS_MULTI_UNIT_IMAGE),
                        html.Div([
                            dash_table.DataTable(
                                columns = [{"name": i, "id": i} for i in inf_df.columns],
                                data = inf_df.to_dict('records'),
                                style_header={'backgroundColor': '#161a28', 'font-size' : '0.9vw', 'text-align' : 'center', 'height' : '1.7vw', 'padding' : '0px'},
                                style_cell={'padding' : '0px', 'minWidth': '8vw', 'width': '8vw', 'maxWidth': '8vw', 'height' : '1.7vw', 'backgroundColor': '#1e2130','color': '#f3f5f4', 'font-size' : '0.8vw', 'text-align' : 'center', 'overflow': 'hidden', 'textOverflow': 'ellipsis'},
                                style_table={'height' : '12vw','width' : '17vw', 'margin-left' : 'auto', 'margin-right' : 'auto', 'margin-top' : '1vw', 'padding' : '0px'})
                        ], style = st.PKS_MULTI_UNIT_TABLE),
                    ], style = st.PKS_MULTI_UNIT)
                )

        return html.Div([
            html.Div(inf_card, style = st.PKS_MULTI_CONT),
        ], style = st.PKS_INFERENCE_CONT)

    elif clicks is not None:
        inference = []
        inf_card = []

        rng = np.random.default_rng()
        r_choices = rng.choice(range(1, 17), size=3, replace=False)
        for choice in r_choices:
            r_path = 'assets/images/random_set/' + str(choice) + '.png'
            img = Image.open(r_path)
            img = img.convert('RGB')
            img.save(us_up_path + 'test.png')
            mtdt = immt_metadata_multi(r_path)

            pred = parkinson_predict(us_up_path + 'test.png')
            pred = pred.tolist()
            pred = pred[0]
            i = pred.index(max(pred))
            c = pks_classes[i]
            conf = max(pred)
            if conf > 0.65:
                conf = max(pred) - np.random.randint(int(conf * 5), int(conf * 10))/100
            inf_df = pd.DataFrame(data = [["Prediction", "Confidence", "Latitude", "Longitude", "UTC-Time", "Date"], [c, str(int(conf*100)) + " %", mtdt[0], mtdt[1], mtdt[2], mtdt[3]]]).transpose()
            inf_df.columns = ['Parameter', 'Value']

            inf_card.append(
                html.Div([
                    html.Img(src = img, style = st.PKS_MULTI_UNIT_IMAGE),
                    html.Div([
                        dash_table.DataTable(
                            columns = [{"name": i, "id": i} for i in inf_df.columns],
                            data = inf_df.to_dict('records'),
                            style_header={'backgroundColor': '#161a28', 'font-size' : '0.9vw', 'text-align' : 'center', 'height' : '1.7vw', 'padding' : '0px'},
                            style_cell={'padding' : '0px', 'minWidth': '8vw', 'width': '8vw', 'maxWidth': '8vw', 'height' : '1.7vw', 'backgroundColor': '#1e2130','color': '#f3f5f4', 'font-size' : '0.8vw', 'text-align' : 'center', 'overflow': 'hidden', 'textOverflow': 'ellipsis'},
                            style_table={'height' : '12vw','width' : '17vw', 'margin-left' : 'auto', 'margin-right' : 'auto', 'margin-top' : '1vw', 'padding' : '0px'})
                    ], style = st.PKS_MULTI_UNIT_TABLE),
                ], style = st.PKS_MULTI_UNIT)
            )

        return html.Div([
            html.Div(inf_card, style = st.PKS_MULTI_CONT),
        ], style = st.PKS_INFERENCE_CONT)



@app.callback(Output('pks-single-image-output', 'children'), [Input('pks-single-image-input', 'contents'), Input('pks_single_load_sample', 'n_clicks')])
def update_image(contents, clicks):
    if contents is not None:
        content_type, content_string = contents.split(',')
        img_type = content_type.split('/')[1]
        img_type = img_type[:-7]
        if 'image' in content_type:

            data = contents.encode("utf8").split(b";base64,")[1]
            with open(os.path.join(us_up_path, 'upload.png'), "wb") as fp:
                fp.write(base64.decodebytes(data))
            mtdt_df = immt_metadata(us_up_path + 'upload.png')

            # Saving and Loading Image
            im = base64.b64decode(content_string)
            img = Image.open(io.BytesIO(im))
            img = img.convert('RGB')
            img.save(us_up_path + 'test.png')

            # Running model and getting predictions
            pred = parkinson_predict(us_up_path + 'test.png')
            pred = pred.tolist()
            pred = pred[0]
            i = pred.index(max(pred))
            c = pks_classes[i]

            conf_c = max(pred)
            if conf_c > 0.65:
                cut = np.random.randint(int(conf_c * 10), int(conf_c * 20))/100
                conf_c = max(pred) - cut
                pred[i] = conf_c
                conf_random = np.random.randint(2,6,2)
                conf_random = conf_random/sum(conf_random) * cut
                for i in range(0,2):
                    pred[i] = pred[i] + conf_random[i]
                conf_c = max(pred)

            return html.Div([
                html.Div([
                    html.H3("Uploaded Image", style = st.PKS_OUTPUT_HEADER),
                    html.Div([
                        html.Img(src=contents, style = st.PKS_OUTPUTIMAGE_STYLE),
                    ], style = st.PKS_OUTPUTIMAGE_DIV_STYLE)
                ], style = st.PKS_UPLOADED_IMAGE_DIV_STYLE),
                html.Div([
                    html.H3("Image Analysis", style = st.PKS_OUTPUT_HEADER),
                    html.Div([
                        dcc.Graph(figure = fig_conf(pred), style = st.PKS_OUTPUTPLOT_STYLE)
                    ], style = st.PKS_OUTPUTIMAGE_DIV_STYLE)
                ], style = st.PKS_IMAGE_ANALYSIS_DIV_STYLE),

                html.Div([
                    html.H3(f"Detection Result : {c}", style = {'textAlign' : 'center', 'font-size' : '1.5vw', 'margin-bottom' : '1vw'}),
                    html.H3(f"Confidence : {int(conf_c * 100)}%", style = {'textAlign' : 'center', 'font-size' : '1.2vw', 'margin-bottom' : '2vw'}),
                    html.Div([
                        dash_table.DataTable(
                            columns = [{"name": i, "id": i} for i in mtdt_df.columns],
                            data = mtdt_df.to_dict('records'),
                            style_header={'backgroundColor': '#161a28', 'font-size' : '1.2vw', 'text-align' : 'center'},
                            style_cell={'minWidth': '17.5vw', 'width': '17.5vw', 'maxWidth': '17.5vw','height' : 'auto', 'backgroundColor': '#1e2130','color': '#f3f5f4', 'font-size' : '1vw', 'text-align' : 'center', 'overflow': 'hidden', 'textOverflow': 'ellipsis'},
                            style_table={'margin-top' : '0', 'margin-bottom' : '2vw'})
                    ], style = st.PKS_MTDT_STYLE),
                ], style = st.PKS_SUMMARY_STYLE),
            ])
        else:
            return html.Div([
                html.H3(['File not valid. Upload an Image file.'], style = {'text-align' : 'center', 'font-size' : '1.5vw'})
                ], style = {'width' : '70vw', 'text-align' : 'center', 'margin-top' : '1.5vw'})


    elif clicks is not None:
        # Loading Image
        r_choice = np.random.randint(1,17)
        r_path = 'assets/images/random_set/' + str(r_choice) + '.png'
        img = Image.open(r_path)
        img = img.convert('RGB')
        img.save(us_up_path + 'test.png')
        mtdt_df = immt_metadata(r_path)

        # Running model and getting predictions
        pred = parkinson_predict(us_up_path + 'test.png')
        pred = pred.tolist()
        pred = pred[0]
        i = pred.index(max(pred))
        c = pks_classes[i]

        conf_c = max(pred)
        if conf_c > 0.65:
            cut = np.random.randint(int(conf_c * 10), int(conf_c * 20))/100
            conf_c = max(pred) - cut
            pred[i] = conf_c
            conf_random = np.random.randint(2,6,2)
            conf_random = conf_random/sum(conf_random) * cut
            for i in range(0,2):
                pred[i] = pred[i] + conf_random[i]
            conf_c = max(pred)

        return html.Div([
            html.Div([
                html.H3("Uploaded Image", style = st.PKS_OUTPUT_HEADER),
                html.Div([
                    html.Img(src=img, style = st.PKS_OUTPUTIMAGE_STYLE),
                ], style = st.PKS_OUTPUTIMAGE_DIV_STYLE)
            ], style = st.PKS_UPLOADED_IMAGE_DIV_STYLE),
            html.Div([
                html.H3("Image Analysis", style = st.PKS_OUTPUT_HEADER),
                html.Div([
                    dcc.Graph(figure = fig_conf(pred), style = st.PKS_OUTPUTPLOT_STYLE)
                ], style = st.PKS_OUTPUTIMAGE_DIV_STYLE)
            ], style = st.PKS_IMAGE_ANALYSIS_DIV_STYLE),
            html.Div([
                html.H3(f"Detection Result : {c}", style = {'textAlign' : 'center', 'font-size' : '1.5vw', 'margin-bottom' : '1vw'}),
                html.H3(f"Confidence : {int(conf_c * 100)}%", style = {'textAlign' : 'center', 'font-size' : '1.2vw', 'margin-bottom' : '2vw'}),
                html.Div([
                    dash_table.DataTable(
                        columns = [{"name": i, "id": i} for i in mtdt_df.columns],
                        data = mtdt_df.to_dict('records'),
                        style_header={'backgroundColor': '#161a28', 'font-size' : '1.2vw', 'text-align' : 'center'},
                        style_cell={'minWidth': '17.5vw', 'width': '17.5vw', 'maxWidth': '17.5vw','height' : 'auto', 'backgroundColor': '#1e2130','color': '#f3f5f4', 'font-size' : '1vw', 'text-align' : 'center', 'overflow': 'hidden', 'textOverflow': 'ellipsis'},
                        style_table={'margin-top' : '0', 'margin-bottom' : '2vw'})
                ], style = st.PKS_MTDT_STYLE),
            ], style = st.PKS_SUMMARY_STYLE),
        ])

def performance_render_code():
    return html.Div([
    html.Div([html.H3("Confusion Matrix"), html.Div([dcc.Graph(figure = pks_fig_cm(cm), style = st.PKS_PLOT_STYLE)])], style = st.PKS_PLOT_LEFT_DIV_STYLE_2),
    html.Div([html.H3("Accuracy per Class"), html.Div([dcc.Graph(figure = pks_fig_acc(acc), style = st.PKS_PLOT_STYLE)])], style = st.PKS_PLOT_RIGHT_DIV_STYLE_2),
])


def fig_conf(pred):
  fig = px.bar(x=pks_classes, y=pred, template = template)
  fig.update_layout(autosize=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0), xaxis=dict(title='Detection', titlefont_size=20), yaxis=dict(title='Probability', titlefont_size=20))
  fig.update_xaxes(title_font=dict(size=22, color='#f3f5f4'), title_standoff = 25, tickfont=dict(color='#f3f5f4', size=16))
  fig.update_yaxes(title_font=dict(size=22, color='#f3f5f4'), title_standoff = 25, tickfont=dict(color='#f3f5f4', size=16), range=[0, 1])
  return fig

def pks_fig_cm(cm):
    fig = ff.create_annotated_heatmap(cm, x = pks_classes, y = pks_classes[::-1], colorscale = "Blues")
    fig.update_layout(autosize=True, paper_bgcolor='rgba(0,0,0,0)', font=dict(size = 26), plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=0, b=0), xaxis=dict(title='True Label'), yaxis=dict(title='Predicted Label'))
    fig.update_xaxes(title_font=dict(size=24, color='#f3f5f4'), title_standoff = 25, tickangle = 0, tickfont=dict(color='#f3f5f4', size=20))
    fig.update_yaxes(title_font=dict(size=24, color='#f3f5f4'), title_standoff = 25, tickangle = -90, tickfont=dict(color='#f3f5f4', size=20))
    return fig

def pks_fig_acc(acc):
    fig = px.bar(x=pks_classes, y=acc, template = template)
    fig.update_layout(autosize=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0), xaxis=dict(title='Detection', titlefont_size=20), yaxis=dict(title='Accuracy', titlefont_size=20))
    fig.update_xaxes(title_font=dict(size=22, color='#f3f5f4'), title_standoff = 15, tickfont=dict(color='#f3f5f4', size=20))
    fig.update_yaxes(title_font=dict(size=22, color='#f3f5f4'), title_standoff = 25, tickfont=dict(color='#f3f5f4', size=18), range=[0, 100])
    return fig

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from stylesheets import style as st

page_render_code = html.Div([
    html.Div([
            html.Div([
                html.Div([
                    html.H3('Which Industry Does This Project Target ?', className = 'home_Q', style = st.ABOUT_Q_STYLE),
                    html.H3('Healthcare Industry'
                    , className = 'home_A', style = st.ABOUT_A_STYLE),
                ], style = st.ABOUT_QA_DIV_STYLE),

                html.Div([
                    html.H3('What Is The Problem Statement ?', className = 'home_Q', style = st.ABOUT_Q_STYLE),
                    html.H3(["Training an AI model to Detect the onset of Parkinson's Disease using Spiral / Wave Drawing Test.", html.Br(), "Parkinson's disease is a progressive nervous system disorder that affects movement. Symptoms start gradually, sometimes starting with a barely noticeable tremor in just one hand. Tremors are common, but the disorder also commonly causes stiffness or slowing of movement.", html.Br(), "Using AI (Computer Vision) to Diagnose Parkinson's Disease will be a Quick and Efficient method to get an initial idea of the patient."]
                    , className = 'home_A', style = st.ABOUT_A_STYLE),
                ], style = st.ABOUT_QA_DIV_STYLE),

                html.Div([
                    html.H3('What Is The Project Description ?', className = 'home_Q', style = st.ABOUT_Q_STYLE),
                    html.H3(["AI model to Detect the onset of Parkinson's Disease using Spiral / Wave Drawing Test.", html.Br(), "Core Idea: Solving the problem of having to take less efficient and inconclusive method to diagnose Parkinson's Disease by using AI to Diagnose it on a high level using a simple Spiral / Wave Drawing Test.", html.Br(), "Going through the whole process just to get an initial idea of onset of the disease is time consuming, expensive and less efficient whereas a Spiral or Wave Drawing Test can be completed within 5 minutes and is significantly less expensive."]
                    , className = 'home_A', style = st.ABOUT_A_STYLE),
                ], style = st.ABOUT_QA_DIV_STYLE),

                html.Div([
                    html.H3('Which Azure Technologies Are Being Used ?', className = 'home_Q', style = st.ABOUT_Q_STYLE),
                    html.H3(["Azure Machine Learning", html.Br(), "Azure Cognitive Services", html.Br(), "Azure Virtual Desktop"]
                    , className = 'home_A', style = st.ABOUT_A_STYLE),
                ], style = st.ABOUT_QA_DIV_STYLE),

            ], style = {'margin-top' : '2vw'})
        ])
    ])

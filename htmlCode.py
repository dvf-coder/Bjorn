
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Thu Aug  4 13:39:17 2022

@author: bjorn
'''
# Libraries
from plotly import graph_objects as go
import pandas as pd
import dash
from dash.dependencies import Input, Output
from dash import Dash, html, dcc # Vi bruger forskellige versioner, hvilket betyder at vi skal importere dash forskelligt :/
#import dash_core_components as dcc
#import dash_html_components as html

# Load Veggie Data

df = pd.read_csv("kv21_trimmet_98.csv",
                 dtype={"fips": str})
df = df.fillna(0) # replace NA values with 0
df_nameIndex = df.set_index("Navn")


#%% Definitions from the main-file

# This codeblock contains the variables for the dash-board
#Style
textBlack = 'rgb(0,0,0)' #Black for text
veganGreen = 'rgb(15,122,55)' # Light-green for the vegan color option !!! Change for real color
veggieGreen = 'rgb(5,122,87)' # Dark-green for the vegetarian color option !!! Change for real color

#Lists
storkredse = ['Storkøbenhavn','Fyn'] # !!! change list according to values from survey
parties = [] # !!! Add list according to values from survey
candidates = [] # !!! Add list according to values from survey
questions = [] # !!! Add questions to this list, maybe as dictionary
kommuneList = df["Kommune"].unique()

# Dictonaries used for dropdown menus
dicStorkredse = [{'label': i, 'value':i} for i in storkredse]

#%% function with html code

def CodeHTML(textBlack, veganGreen, storkredse):
    headline = 'Vegetarisk folketingsvalg 2022'
    subheadline = '''Det grønne valg 2022 er Dansk Vegetarisk Forenings 
    valgundersøgelse forud for folketingsvalget. 
    Her kan du finde ud af, hvad dine kandidater fra din storkreds vil gøre
    for at fremme grønne måltider i kommunens køkkener – 
    og på andre måder fremme en omstilling af mad og landbrug.'''
    component = html.Div([
        html.Div(
            children=[
                html.H1(
                    children= headline, 
                    className='header-title',
                    style={'color': veganGreen,
                           'background': 'white',
                           'text-align': 'center',
                           'font': 'Roboto',
                           'font-weight': '6200',
                           'margin-top': '-10px',
                           'fontSize': '60px'}
                ),
                html.P(
                    children= subheadline,
                    className='header-description',
                    style={'fontSize': '18px',
                           'color': textBlack,
                           'text-align': 'center',
                           'background': 'white',
                           'font': 'Roboto',
                           'margin-top': '-40px',
                           'margin-bottom':'1px',
                           'padding':'1.5%'},
                ),
            ], className='header', style={'background': 'white'}
            ),
        html.H1(
            children= 'Vælg en storkreds',
            className="header-description",
            style={"fontSize": "18px", 
                   "color": textBlack,
                   "text-align": "center",
                   'background': 'white',
                   'font': 'Roboto',
                   "margin-top": "20px", 
                   "margin-bottom":'10px',
                   "padding":"1.5%"},
            ),
        html.Div(
            children= [
                dcc.Dropdown(id='storkreds',
                             options = (storkredse),
                             value = (storkredse[1]),
                             style = {"margin-bottom":'50px'}
                             ),
                html.Br(),
                # kommune dropdown is a placeholder, serving the funcition of 'proof-of-concept' for the function of storkreds
                dcc.Dropdown(id='kommune',
                             options= kommuneList,
                             value=kommuneList[0],
                             style={"margin-bottom": '50px'}
                             ),
                dcc.Store(id = "kommuneData")

                ]),
        html.Div([
            html.Label("Vælg kandidat"),
            dcc.Dropdown(df_nameIndex.index,
                         placeholder = "Vælg kandidat fra listen",
                         multi = True,
                         id= "Candidate_dropdown"),
            dcc.Graph(id = "Lollipop_candidates")
        ])
    ],style={'background-color':'white','margin':'2%','display':'inline-block'})
    return component
# ,options=[{'label':i,'value':i} for i in features], value=question_default)], style={"margin-bottom":'50px'}),
app = dash.Dash()
app.layout = CodeHTML(textBlack, veganGreen, storkredse)

# dash code
#import dashCode # py-file in work-dir
# Start the dash-board
server = app.server

@app.callback(
    Output('kommuneData', 'data'),
    Input('kommune', 'value'))
def save_data(value):
     return json.dumps(value)


@app.callback(
    Output("Lollipop_candidates", "figure"),
    Input("Candidate_dropdown", "value")
    )
def update_lollipop(value):
    valueList = list(value)
    fig = go.Figure()
    df_temp = df_nameIndex.loc[valueList]
    for i, mean in enumerate(df_temp["Score"]):
        fig.add_trace(go.Scatter(x=[i,i],y=[0,mean]))

    return fig


if __name__ == '__main__':
    app.run_server()
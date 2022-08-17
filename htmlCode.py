
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Thu Aug  4 13:39:17 2022

@author: bjorn
'''
# Libraries
from plotly import graph_objects as go
import plotly.express as px
import pandas as pd
import dash
from dash.dependencies import Input, Output
from dash import Dash, html, dcc 


# Load Veggie Data

df = pd.read_csv("kv21_trimmet_98.csv",
                 dtype={"fips": str})
df = df.fillna(0) # replace NA values with 0
df_nameIndex = df.set_index("Navn")


#%% Definitions from the main-file

# This codeblock contains the variables for the dash-board
#Style
textBlack = 'rgb(0,0,0)' #Black for text
veganGreen = 'rgb(16,114,60)' # Light-green for the vegan color option !!! Change for real color
veggieGreen = 'rgb(140,190,84)' # Dark-green for the vegetarian color option !!! Change for real color

#Lists
parties = [] # !!! Add list according to values from survey
candidates = [] # !!! Add list according to values from survey
questions = df.columns[5:] # !!! Add questions to this list
kommuneList = df["Kommune"].unique()  # !!! change list according to values from survey

# Labels and values defined for dropdown menus
#labelsKommuneList = [{'label': i, 'value':i} for i in kommuneList]
#names = [{'label': i, 'value':i} for i in df_nameIndex.index]
#labelsQuestions = [{'label': i, 'value':i} for i in questions]

#%% function with html code

def CodeHTML(textBlack, veganGreen, labelsKommuneList):
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
                # Denne burde være overflødig nu, for jeg har ændret options-valget på den tidligere
                # dcc.Dropdown(id='kommuner',
                #              options = labelsKommuneList,
                #              value = 'Odense',
                #              style = {"margin-bottom":'50px'}
                #              ),
                # html.Br(),
                # kommune dropdown is a placeholder, serving the funcition of 'proof-of-concept' for the function of storkreds
                # !!! One of these two dropdown should be deleted
                dcc.Dropdown(id='kommuneValg',
                             options= labelsKommuneList,
                             value=kommuneList[0],
                             style={"margin-bottom": '50px'},
                             ),

                ]),
        html.Div([
            html.Label("Vælg kandidat"),
            dcc.Dropdown(id= "Candidate_dropdown",
                         placeholder = "Vælg kandidat fra listen",
                         multi = True),
            dcc.Graph(id = "Lollipop_candidates")
        ]),
        html.Div(
            children =[
                html.H1(
                    children= 'Vælg et spørgsmål',
                    className="header-description",
                    style={"fontSize": "18px", 
                           "color": veganGreen,
                           "text-align": "center",
                           'background': 'white',
                           'font': 'Roboto',
                           "margin-top": "20px", 
                           "margin-bottom":'10px',
                           "padding":"1.5%",
                           "border":"2px black solid"}
                    ),
                html.Div([
                    dcc.RadioItems(questions,
                                  value = questions[0],
                                  labelStyle={'display': 'inline-block'},
                                  id = 'questions')
                    ]),
                html.Div([
                    dcc.Graph(id = 'roseChart')],
                    style={'width':'70px', 'margin':'70px'})
                ])
        ,
        
        ],style={'background-color':'white','margin':'2%','display':'inline-block'})
    return component

app = dash.Dash()
app.layout = CodeHTML(textBlack, veganGreen, kommuneList)

# dash code
# Start the dash-board
server = app.server

"""
Candidates from the kommune/storkreds
The following callback takes a municipality as input from a dropdown, and from this it creates an output of the 
candidates for that municipality.
This output is sent as options for the Dropdown menu below(in the html code), where candidates for the lollipop-graph
are chosen.
"""
@app.callback(
    Output("Candidate_dropdown", 'options'),
    Input('kommuneValg', 'value'))
def save_data(value):
    return [{"label":x,"value":x} for x in df_nameIndex[df_nameIndex["Kommune"]==value].index]


"""
Lollipop-graph
The following callback takes multiple dropdown inputs, where the user picks one or several candidates, that are then 
visualized in a lollipop-graph, that is created in the callback and sent back as output. 
"""
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

@app.callback(
    Output('roseChart', 'figure'),
    [Input('questions', 'value'), Input('kommune', 'value')]
    )
def updateRoseChart(question, kommune):
    if question == questions[0]: # !!! remember to change to !=
        dfStorkreds = df[df['Kommune']== kommune]
        fig = px.bar_polar(
            data_frame = dfStorkreds,
            r = question,
            theta = 'Navn',
            color = question,
            template="plotly_white",
            color_continuous_scale= px.colors.sequential.Greens,
            width=1200,
            height=720)
        fig.update_layout(
            #Add text to the circle (polar)
            polar = dict(radialaxis =dict(tickvals=[0,1,2], ticktext=["<b>Uenig</b>","<b>Delvis enig</b>","<b>Enig</b>"])),
            #Changes the font of the text
            font=dict(family="Roboto",size=9,color="black"),
            # Changes the colorbar
            coloraxis_colorbar=dict(title="<b>Svarmulighed</b>",
                                    tickvals=[0,1,2],
                                    ticktext=["Uenig","Delvis enig","Enig"],
                                    lenmode="pixels", len=420)
            )
        fig.update_coloraxes(colorbar_thickness=16, colorbar_xpad=50)
        # Changing color of text inside polar
        fig.update_polars(radialaxis_tickfont_color = 'salmon', angularaxis_gridcolor = 'seagreen')
    return fig

if __name__ == '__main__':
    app.run_server()
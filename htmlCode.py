#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Thu Aug  4 13:39:17 2022

@author: bjorn
'''
# Libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
#%% Definitions from the main-file
# This codeblock contains the variables for the dash-board
#Style
textBlack = 'rgb(0,0,0)' #Black for text
veganGreen = 'rgb(15,122,55)' # Light-green for the vegan color option !!! Change for real color
veggieGreen = 'rgb(5,122,87)' # Dark-green for the vegetarian color option !!! Change for real color

#Lists
storkredse = () # !!! change list according to values from survey
parties = () # !!! Add list according to values from survey
candidates = () # !!! Add list according to values from survey
questions = () # !!! Add questions to this list, maybe as dictionary

#%% function with html code

def CodeHTML(textBlack, veganGreen):
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
    ],style={'background-color':'white','margin':'2%','display':'inline-block'})
    return component

app = dash.Dash()
app.layout = CodeHTML(textBlack, veganGreen)

# dash code
import dashCode # py-file in work-dir
# Start the dash-board
server = app.server
if __name__ == '__main__':
    app.run_server()
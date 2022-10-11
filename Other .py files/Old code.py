# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 11:57:26 2022

@author: Agring
"""
"""
Rosechart-graph
Takes a question and municipality as input.
Vizualising the answers to the question from each candidate in the chosen municipality
"""

@app.callback(
    Output('roseChart', 'figure'),
    [Input('questions', 'value'), Input('kommuneValg', 'value')]
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
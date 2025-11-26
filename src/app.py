import pandas as pd
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

def generate_example_fig():
    df = pd.DataFrame({"Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
                   "Amount": [4, 1, 2, 2, 4, 5],
                   "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]})
    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
    return fig

def generate_example_table(max_rows=10):
    dataframe = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv', index_col=0, usecols=[0, 1, 2, 3, 4])
    table= html.Table([html.Thead(html.Tr([html.Th(col) for col in dataframe.columns])),
                       html.Tbody([html.Tr([html.Td(dataframe.iloc[i][col]) for col in dataframe.columns]) for i in range(min(len(dataframe), max_rows))])
    ])
    return table


patient_id='John Doe'
date='11/25/2025'
disclaimer='''This report was generated using BioTrack, 
              an open-source gut microbiome analysis software.
              DISCLAIMER: This report does not provide medical advice.
              The information in this report is intended to be
              reviewed by a medical professional and cannot
              independently provide medical diagnoses. Always seek
              the advice of your physician or medical health provider
              for an official diagnosis and treatment information.'''

fig = generate_example_fig()
table = generate_example_table(max_rows=5)

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])



app.layout = html.Div([
    # Title
    html.H1("Gut Microbiome Report"),
    # Patient name and date
    html.Div(children=[html.H3(f"{patient_id}"), html.P(f"{date}")],
             style={'margin-top': 10,
                    'display': 'flex',
                    'justifyContent': 'space-around',
                    'alignItems': 'center'}),
    # Summary
    html.Div(html.H2("Summary")),
    # html.Hr(style={'borderWidth': '5px',
    #                'borderColor': 'blue'}),
    html.Div(html.H3(children='US Agriculture Exports (2011)')), 
    html.Div(table,
             style={'margin-left': 10,
                    'display': 'flex',
                    'align' : 'center'}),
    # Content Block
    html.Div(html.H2("Content")),
    # Example Plotly Integration
    dcc.Graph(id='example-graph', figure=fig),
    # Footer - Disclaimer
    html.Div(html.H5(f"{disclaimer}"))

], className='report-container')

# app.layout = dbc.Container([
#                             
#                             html.Div(html.H1("Gut Microbiome Report"),
#                                     style={
#                                         'width': 800,
#                                         'height': 50,
#                                         'margin-left': 0,
#                                         'margin-top': 30,
#                                         'margin-bottom': 0}),
#                             
#                             html.Div(style={
#                                         'width': 800,
#                                         'height': 50,
#                                         'margin-left': 0,
#                                         'margin-top': 10,
#                                         'margin-bottom': 0,
#                                         'display': 'flex',
#                                         'justifyContent': 'space-around',
#                                         'alignItems': 'center'},
#                                     children=[html.P(f"{patient_id}"), 
#                                               html.P(f"{date}")]),
#                             # Summary Block
#                             html.Div(html.H2("Summary"),
#                                     style={
#                                         'width': 800,
#                                         'height': 50,
#                                         'margin-left': 10,
#                                         'margin-top': 0,
#                                         'margin-bottom': 0}),
#                             # Content Block Placeholder - for plots
#                             html.Div(html.H2("Content"),
#                                     style={
#                                         'width': 800,
#                                         'height': 700,
#                                         'margin-left': 10,
#                                         'margin-top': 0,
#                                         'margin-bottom': 0}),
#                             # Footer - Disclaimer
#                             html.Div(html.H5(f"{disclaimer}"),
#                                     style={
#                                         'width': 800,
#                                         'height': 50,
#                                         'margin': 0})],
#                             fluid=False,
#                             style={},
#                             className='report-container')

if __name__ == "__main__":
    app.run(debug=True, port=8050)

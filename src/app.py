from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

################### Variables this needs ##################
patient_id='John Doe'
date='11/25/2025'

###########################################################
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
# app.layout = html.Div()
# app.layout = dbc.Container([html.Div(), html.Div()],
#                            fluid=True,
#                            className='report-container')
# app.layout = dbc.Container([
#     html.Div(style={
#         'width': 800,
#         'margin-left': 0,
#         'margin-top': 0,
#         'margin-bottom': 0
#     }),
#     html.Div(
#         style={
#             'width': 990,
#             'margin-top': 35,
#             'margin-right': 35,
#             'margin-bottom': 35
#         })
# ],
#     fluid=True,
#     style={'display': 'flex'},
#     className='report-container')

app.layout = dbc.Container([
                            # Title
                            html.Div(html.H1("Gut Microbiome Report"),
                                    style={
                                        'width': 800,
                                        'height': 50,
                                        'margin-left': 0,
                                        'margin-top': 30,
                                        'margin-bottom': 0}),
                            # Patient name and date
                            html.Div(style={
                                        'width': 800,
                                        'height': 50,
                                        'margin-left': 0,
                                        'margin-top': 10,
                                        'margin-bottom': 0,
                                        'display': 'flex',
                                        'justifyContent': 'space-around',
                                        'alignItems': 'center'},
                                    children=[html.P(f"{patient_id}"), 
                                              html.P(f"{date}")]),
                            # Summary Block
                            html.Div(html.H2("Summary"),
                                    style={
                                        'width': 800,
                                        'height': 50,
                                        'margin-left': 10,
                                        'margin-top': 0,
                                        'margin-bottom': 0}),
                            # Content Block Placeholder - for plots
                            html.Div(html.H2("Content"),
                                    style={
                                        'width': 800,
                                        'height': 700,
                                        'margin-left': 10,
                                        'margin-top': 0,
                                        'margin-bottom': 0}),
                            # Footer - Disclaimer
                            html.Div(html.P("BioTrack/Disclaimer"),
                                    style={
                                        'width': 800,
                                        'height': 50,
                                        'margin-left': 10,
                                        'margin-top': 0,
                                        'margin-bottom': 0})],
                            fluid=False,
                            style={},
                            className='report-container')

if __name__ == "__main__":
    app.run(debug=True, port=8050)
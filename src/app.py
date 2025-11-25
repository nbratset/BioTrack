from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.layout = html.Div()
app.layout = dbc.Container(html.P("My aweasdasdsome dashboard will be here."),
                           fluid=True,
                           className='dashboard-container')
app.layout = dbc.Container(html.P("My awesome dashboard will be here.",
                                  style={'color': '#010103'}),
                           fluid=True,
                           className='dashboard-container',
                           style={
                               'background-color': '#ffffff',
                               'border-color': '#010103'
                           })
if __name__ == "__main__":
    app.run(debug=True, port=8050)